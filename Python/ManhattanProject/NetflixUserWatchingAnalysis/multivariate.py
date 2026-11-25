import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.formula.api as smf

# ==============================================================================
# 0. LOAD & PREPARE DATA
# ==============================================================================
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
df = pd.read_csv(BASE_DIR / "netflix_user_behavior_dataset.csv")

# Binary churn indicator
df["churn_flag"] = (df["churned"].astype(str).str.strip().str.lower() == "yes").astype(int)

# Standardized feature tiers for interpretable multi-way slicing
df["fee_tier"] = pd.cut(
    df["monthly_fee"],
    bins=[0, 9.99, 13.99, 100],
    labels=["Budget ($7.99)", "Mid ($12.99)", "Premium Fee ($15.99)"]
)
df["watch_tier"] = pd.qcut(
    df["avg_watch_time_minutes"],
    q=3,
    labels=["Low Watch", "Medium Watch", "High Watch"]
)
df["recency_tier"] = pd.qcut(
    df["days_since_last_login"],
    q=3,
    labels=["Recent Login", "Moderate Gap", "Long Inactive"]
)
df["age_group"] = pd.cut(
    df["age"],
    bins=[17, 25, 35, 45, 55, 100],
    labels=["18-25", "26-35", "36-45", "46-55", "56+"]
)
df["binge_tier"] = pd.qcut(
    df["binge_watch_sessions"],
    q=3,
    labels=["Low Binge", "Med Binge", "High Binge"]
)
df["interaction_tier"] = pd.qcut(
    df["content_interactions"],
    q=3,
    labels=["Low Interact", "Med Interact", "High Interact"]
)
df["ctr_tier"] = pd.qcut(
    df["recommendation_click_rate"],
    q=3,
    labels=["Low CTR", "Med CTR", "High CTR"]
)
df["completion_tier"] = pd.qcut(
    df["completion_rate"],
    q=3,
    labels=["Low Completion", "Med Completion", "High Completion"]
)
df["rating_tier"] = pd.cut(
    df["rating_given"],
    bins=[0, 2.5, 3.5, 5.0],
    labels=["Low Rating (<=2.5)", "Neutral (2.6-3.5)", "High Rating (>3.5)"]
)


# ==============================================================================
# 3.1 PROFILING CHURNED USERS
# subscription_type + monthly_fee + avg_watch_time_minutes + days_since_last_login
# ==============================================================================
print("\n=== 3.1 CHURN PROFILES (TOP 10 BY CHURN RATE, MIN 100 USERS) ===")
churn_profiles = (
    df.groupby(["subscription_type", "fee_tier", "watch_tier", "recency_tier"], observed=False)
    .agg(
        user_count=("user_id", "count"),
        churn_rate=("churn_flag", "mean"),
        avg_fee=("monthly_fee", "mean"),
        avg_watch_mins=("avg_watch_time_minutes", "mean"),
        avg_days_inactive=("days_since_last_login", "mean"),
    )
    .reset_index()
)

top_churn_profiles = (
    churn_profiles[churn_profiles["user_count"] >= 100]
    .sort_values(["churn_rate", "user_count"], ascending=[False, False])
)
print(top_churn_profiles.head(10).to_string(index=False))

# Logistic regression with interaction terms to test multivariate churn drivers
churn_logit = smf.logit(
    "churn_flag ~ C(subscription_type) * monthly_fee + avg_watch_time_minutes + days_since_last_login + avg_watch_time_minutes:days_since_last_login",
    data=df
).fit(disp=False)
print("\nChurn Logistic Regression Summary (p-values):")
print(churn_logit.pvalues.round(4))


# ==============================================================================
# 3.2 CONTENT ENGAGEMENT AND PLATFORM STICKINESS
# primary_device + age_group + binge_watch_sessions + content_interactions -> completion_rate
# ==============================================================================
print("\n=== 3.2 MEAN COMPLETION RATE BY DEVICE, AGE GROUP, BINGE & INTERACTIONS ===")
engagement_table = (
    df.groupby(["primary_device", "age_group", "binge_tier", "interaction_tier"], observed=False)
    .agg(
        users=("user_id", "count"),
        mean_completion=("completion_rate", "mean"),
        std_completion=("completion_rate", "std"),
        mean_binge=("binge_watch_sessions", "mean"),
        mean_interactions=("content_interactions", "mean"),
    )
    .reset_index()
)

# Pivot for quick side-by-side comparison across binge & interaction tiers
engagement_pivot = df.pivot_table(
    index=["primary_device", "age_group"],
    columns=["binge_tier", "interaction_tier"],
    values="completion_rate",
    aggfunc="mean",
    observed=False
)
print(engagement_pivot.round(2).head(10).to_string())

# OLS regression testing main effects and interactions on completion_rate
eng_ols = smf.ols(
    "completion_rate ~ C(primary_device) + C(age_group) + binge_watch_sessions * content_interactions",
    data=df
).fit()
print("\nCompletion Rate OLS R-squared:", round(eng_ols.rsquared, 5), "| F-test p-value:", round(eng_ols.f_pvalue, 4))


# ==============================================================================
# 3.3 PRICE SENSITIVITY ACROSS REGIONS
# country + monthly_fee + subscription_type -> premium vs. budget tier adoption
# ==============================================================================
print("\n=== 3.3 REGIONAL SUBSCRIPTION MIX, FEE & CHURN ===")
regional_pricing = (
    df.groupby(["country", "subscription_type"], observed=False)
    .agg(
        users=("user_id", "count"),
        avg_monthly_fee=("monthly_fee", "mean"),
        churn_rate=("churn_flag", "mean"),
    )
    .reset_index()
)
regional_pricing["country_share_pct"] = (
    regional_pricing["users"]
    / regional_pricing.groupby("country")["users"].transform("sum")
    * 100
).round(2)

# Wide view: share (%) of each subscription_type per country
tier_share_wide = regional_pricing.pivot(
    index="country", columns="subscription_type", values="country_share_pct"
).reset_index()

# Average fee and churn rate by country
country_summary = (
    df.groupby("country", observed=False)
    .agg(
        total_users=("user_id", "count"),
        avg_fee=("monthly_fee", "mean"),
        overall_churn_rate=("churn_flag", "mean"),
    )
    .reset_index()
)

price_sensitivity_df = (
    country_summary
    .merge(tier_share_wide, on="country")
    .assign(premium_to_basic_ratio=lambda d: (d["Premium"] / d["Basic"].replace(0, np.nan)).round(2))
    .sort_values("Premium", ascending=False)
)
print(price_sensitivity_df.to_string(index=False))

# Chi-square test of independence between country and subscription_type
ct_country_sub = pd.crosstab(df["country"], df["subscription_type"])
chi2, p_val, dof, _ = stats.chi2_contingency(ct_country_sub)
print(f"\nChi-Square (country vs subscription_type): chi2={chi2:.2f}, dof={dof}, p={p_val:.4f}")


# ==============================================================================
# 3.4 RECOMMENDATION TRUST DYNAMICS
# recommendation_click_rate + completion_rate + rating_given -> high-value satisfied segments
# ==============================================================================
print("\n=== 3.4 RECOMMENDATION TRUST SEGMENTS ===")
trust_segments = (
    df.groupby(["ctr_tier", "completion_tier", "rating_tier"], observed=False)
    .agg(
        users=("user_id", "count"),
        avg_ctr=("recommendation_click_rate", "mean"),
        avg_completion=("completion_rate", "mean"),
        avg_rating=("rating_given", "mean"),
        avg_watch_mins=("avg_watch_time_minutes", "mean"),
        churn_rate=("churn_flag", "mean"),
    )
    .reset_index()
)

# Composite trust & satisfaction score (min-max scaled within each metric)
for col in ["avg_ctr", "avg_completion", "avg_rating"]:
    col_min, col_max = trust_segments[col].min(), trust_segments[col].max()
    trust_segments[f"{col}_norm"] = (
        (trust_segments[col] - col_min) / (col_max - col_min)
        if col_max > col_min else 0.5
    )

trust_segments["trust_satisfaction_score"] = (
    (trust_segments["avg_ctr_norm"] + trust_segments["avg_completion_norm"] + trust_segments["avg_rating_norm"]) / 3
).round(3)

trust_segments = trust_segments.sort_values("trust_satisfaction_score", ascending=False)
print(
    trust_segments[
        ["ctr_tier", "completion_tier", "rating_tier", "users", "avg_ctr", "avg_completion", "avg_rating", "churn_rate", "trust_satisfaction_score"]
    ].head(10).to_string(index=False)
)

# Flag explicit High-Trust / High-Satisfaction cohort
high_trust_users = df[
    (df["recommendation_click_rate"] >= df["recommendation_click_rate"].quantile(0.67))
    & (df["completion_rate"] >= df["completion_rate"].quantile(0.67))
    & (df["rating_given"] >= 4.0)
]
print(
    f"\nHigh-Trust & High-Satisfaction Cohort: {len(high_trust_users):,} users "
    f"({len(high_trust_users)/len(df)*100:.2f}% of base) | "
    f"Churn Rate: {high_trust_users['churn_flag'].mean()*100:.2f}% vs "
    f"Rest: {df.loc[~df.index.isin(high_trust_users.index), 'churn_flag'].mean()*100:.2f}%"
)