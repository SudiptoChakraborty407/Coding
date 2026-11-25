from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats

# ==============================================================================
# 0. LOAD & PREPARE DATA
# ==============================================================================
BASE_DIR = Path(__file__).resolve().parent if "__file__" in globals() else Path(".")
df = pd.read_csv(BASE_DIR / "netflix_user_behavior_dataset.csv")

# Binary churn flag: 1 = churned ('Yes'), 0 = retained ('No')
df["churn_flag"] = (
    df["churned"].astype(str).str.strip().str.lower() == "yes"
).astype(int)

# Standard age brackets for genre clustering
df["age_group"] = pd.cut(
    df["age"],
    bins=[17, 24, 34, 44, 54, 100],
    labels=["18-24", "25-34", "35-44", "45-54", "55+"],
)


# ==============================================================================
# 2.1 SUBSCRIPTION TIER VS. CHURN RISK & PRICE SENSITIVITY
# ==============================================================================
print("\n" + "=" * 75)
print("2.1 SUBSCRIPTION TIER VS. CHURN RISK & PRICE SENSITIVITY")
print("=" * 75)

tier_order = ["Basic", "Standard", "Premium"]
tier_churn = (
    df.groupby("subscription_type", observed=False)
    .agg(
        users=("user_id", "count"),
        churned_users=("churn_flag", "sum"),
        churn_rate_pct=("churn_flag", lambda s: round(s.mean() * 100, 2)),
        avg_monthly_fee=("monthly_fee", "mean"),
    )
    .reindex(tier_order)
)
tier_churn["avg_monthly_fee"] = tier_churn["avg_monthly_fee"].round(2)
print("Churn by Subscription Tier:")
print(tier_churn.to_string())

# Chi-square test: subscription_type vs. churned
ct_tier_churn = pd.crosstab(df["subscription_type"], df["churned"])
chi2_tier, p_tier, dof_tier, _ = stats.chi2_contingency(ct_tier_churn)
print(f"\nChi-Square (subscription_type vs churned): chi2={chi2_tier:.4f}, dof={dof_tier}, p={p_tier:.4f}")

# Price sensitivity check: monthly_fee vs. churn_flag (within and across tiers)
fee_churn = (
    df.groupby("monthly_fee", observed=False)
    .agg(
        users=("user_id", "count"),
        churn_rate_pct=("churn_flag", lambda s: round(s.mean() * 100, 2)),
    )
)
print("\nChurn Rate by Monthly Fee:")
print(fee_churn.to_string())

r_fee, p_fee = stats.pointbiserialr(df["churn_flag"], df["monthly_fee"])
print(f"Point-Biserial Correlation (monthly_fee vs churn_flag): r={r_fee:.4f}, p={p_fee:.4f}")


# ==============================================================================
# 2.2 WATCH TIME VS. CHURN STATUS & VIEWING THRESHOLDS
# ==============================================================================
print("\n" + "=" * 75)
print("2.2 WATCH TIME VS. CHURN STATUS & VIEWING THRESHOLDS")
print("=" * 75)

# Compare watch metrics between retained and churned users
watch_by_churn = df.groupby("churned", observed=False)[
    ["avg_watch_time_minutes", "binge_watch_sessions", "watch_sessions_per_week"]
].agg(["mean", "median", "std"])
print("Watch Metrics by Churn Status:")
print(watch_by_churn.round(2).to_string())

# Correlations with churn_flag
for col in ["avg_watch_time_minutes", "binge_watch_sessions", "watch_sessions_per_week"]:
    r_val, p_val = stats.pointbiserialr(df["churn_flag"], df[col])
    t_val, p_t = stats.ttest_ind(
        df.loc[df["churn_flag"] == 1, col],
        df.loc[df["churn_flag"] == 0, col],
        equal_var=False,
    )
    print(f"{col}: r={r_val:.4f} (p={p_val:.4f}) | Welch t={t_val:.4f} (p={p_t:.4f})")

# Daily watch time thresholds (avg_watch_time_minutes ranges 10-299)
watch_bins = pd.cut(
    df["avg_watch_time_minutes"],
    bins=[0, 30, 60, 120, 180, 240, np.inf],
    labels=["0-30m", "31-60m", "61-120m", "121-180m", "181-240m", "241m+"],
)
watch_thresh = (
    df.groupby(watch_bins, observed=False)
    .agg(
        users=("user_id", "count"),
        churn_rate_pct=("churn_flag", lambda s: round(s.mean() * 100, 2)),
        retention_rate_pct=("churn_flag", lambda s: round((1 - s.mean()) * 100, 2)),
    )
)
watch_thresh["pct_change_vs_prev_bucket"] = watch_thresh["churn_rate_pct"].diff().round(2)
print("\nChurn Rate Across Daily Watch Time Thresholds:")
print(watch_thresh.to_string())

# Binge watch session thresholds (binge_watch_sessions ranges 0-14)
binge_bins = pd.cut(
    df["binge_watch_sessions"],
    bins=[-1, 0, 2, 5, 8, 11, np.inf],
    labels=["0", "1-2", "3-5", "6-8", "9-11", "12+"],
)
binge_thresh = (
    df.groupby(binge_bins, observed=False)
    .agg(
        users=("user_id", "count"),
        churn_rate_pct=("churn_flag", lambda s: round(s.mean() * 100, 2)),
        retention_rate_pct=("churn_flag", lambda s: round((1 - s.mean()) * 100, 2)),
    )
)
binge_thresh["pct_change_vs_prev_bucket"] = binge_thresh["churn_rate_pct"].diff().round(2)
print("\nChurn Rate Across Binge Watch Session Thresholds:")
print(binge_thresh.to_string())


# ==============================================================================
# 2.3 DEVICE PREFERENCE VS. ENGAGEMENT (COMPLETION & WATCH TIME)
# ==============================================================================
print("\n" + "=" * 75)
print("2.3 DEVICE PREFERENCE VS. ENGAGEMENT")
print("=" * 75)

# Primary device vs. completion_rate and avg_watch_time_minutes
device_eng = (
    df.groupby("primary_device", observed=False)
    .agg(
        users=("user_id", "count"),
        share_pct=("user_id", lambda s: round(len(s) / len(df) * 100, 2)),
        avg_completion_rate=("completion_rate", "mean"),
        median_completion_rate=("completion_rate", "median"),
        avg_watch_mins=("avg_watch_time_minutes", "mean"),
        avg_devices_used=("devices_used", "mean"),
    )
    .sort_values("avg_watch_mins", ascending=False)
)
print("Engagement by Primary Device:")
print(device_eng.round(2).to_string())

# One-way ANOVA across primary_device for completion_rate & avg_watch_time_minutes
dev_groups_comp = [grp["completion_rate"].values for _, grp in df.groupby("primary_device")]
dev_groups_watch = [grp["avg_watch_time_minutes"].values for _, grp in df.groupby("primary_device")]
f_comp, p_comp = stats.f_oneway(*dev_groups_comp)
f_watch, p_watch = stats.f_oneway(*dev_groups_watch)
print(f"\nANOVA primary_device -> completion_rate: F={f_comp:.4f}, p={p_comp:.4f}")
print(f"ANOVA primary_device -> avg_watch_time_minutes: F={f_watch:.4f}, p={p_watch:.4f}")

# Direct comparison: Mobile vs. Smart TV
mobile_df = df[df["primary_device"] == "Mobile"]
tv_df = df[df["primary_device"] == "Smart TV"]
t_mob_tv_comp, p_mob_tv_comp = stats.ttest_ind(
    mobile_df["completion_rate"], tv_df["completion_rate"], equal_var=False
)
t_mob_tv_watch, p_mob_tv_watch = stats.ttest_ind(
    mobile_df["avg_watch_time_minutes"], tv_df["avg_watch_time_minutes"], equal_var=False
)
print(
    f"Mobile vs. Smart TV | Completion: {mobile_df['completion_rate'].mean():.2f}% vs "
    f"{tv_df['completion_rate'].mean():.2f}% (t={t_mob_tv_comp:.4f}, p={p_mob_tv_comp:.4f}) | "
    f"Watch mins: {mobile_df['avg_watch_time_minutes'].mean():.2f} vs "
    f"{tv_df['avg_watch_time_minutes'].mean():.2f} (t={t_mob_tv_watch:.4f}, p={p_mob_tv_watch:.4f})"
)

# Number of devices_used vs. engagement
dev_count_eng = (
    df.groupby("devices_used", observed=False)
    .agg(
        users=("user_id", "count"),
        avg_completion_rate=("completion_rate", "mean"),
        avg_watch_mins=("avg_watch_time_minutes", "mean"),
    )
    .round(2)
)
print("\nEngagement by Number of Devices Used (devices_used):")
print(dev_count_eng.to_string())

r_dev_comp, p_dev_comp = stats.pearsonr(df["devices_used"], df["completion_rate"])
r_dev_watch, p_dev_watch = stats.pearsonr(df["devices_used"], df["avg_watch_time_minutes"])
print(f"Correlation devices_used vs completion_rate: r={r_dev_comp:.4f}, p={p_dev_comp:.4f}")
print(f"Correlation devices_used vs avg_watch_time_minutes: r={r_dev_watch:.4f}, p={p_dev_watch:.4f}")


# ==============================================================================
# 2.4 RECOMMENDATION EFFECTIVENESS
# ==============================================================================
print("\n" + "=" * 75)
print("2.4 RECOMMENDATION EFFECTIVENESS")
print("=" * 75)

rec_cols = ["recommendation_click_rate", "rating_given", "content_interactions"]
print("Pearson Correlation Matrix:")
print(df[rec_cols].corr(method="pearson").round(4).to_string())

print("\nSpearman Rank Correlation Matrix:")
print(df[rec_cols].corr(method="spearman").round(4).to_string())

# Exact pairwise r & p-values
for target in ["rating_given", "content_interactions"]:
    r_p, p_p = stats.pearsonr(df["recommendation_click_rate"], df[target])
    r_s, p_s = stats.spearmanr(df["recommendation_click_rate"], df[target])
    print(
        f"recommendation_click_rate vs {target}: "
        f"Pearson r={r_p:.4f} (p={p_p:.4f}) | Spearman rho={r_s:.4f} (p={p_s:.4f})"
    )

# Quartile breakdown of recommendation_click_rate
df["ctr_quartile"] = pd.qcut(
    df["recommendation_click_rate"],
    q=4,
    labels=["Q1 (Lowest CTR)", "Q2", "Q3", "Q4 (Highest CTR)"],
)
ctr_summary = (
    df.groupby("ctr_quartile", observed=False)
    .agg(
        users=("user_id", "count"),
        avg_ctr=("recommendation_click_rate", "mean"),
        avg_rating=("rating_given", "mean"),
        avg_interactions=("content_interactions", "mean"),
    )
    .round(2)
)
print("\nMean Rating & Interactions Across CTR Quartiles:")
print(ctr_summary.to_string())


# ==============================================================================
# 2.5 AGE VS. CONTENT PREFERENCE (AND GENDER SEGMENTS)
# ==============================================================================
print("\n" + "=" * 75)
print("2.5 AGE VS. CONTENT PREFERENCE (GENRE BY AGE GROUP & GENDER)")
print("=" * 75)

# Favorite genre row-wise % across age_group
genre_by_age_pct = (
    pd.crosstab(df["age_group"], df["favorite_genre"], normalize="index") * 100
).round(2)
print("Favorite Genre Share (%) Within Each Age Group:")
print(genre_by_age_pct.to_string())

# Chi-square test: age_group vs. favorite_genre
ct_age_genre = pd.crosstab(df["age_group"], df["favorite_genre"])
chi2_age, p_age, dof_age, _ = stats.chi2_contingency(ct_age_genre)
print(f"\nChi-Square (age_group vs favorite_genre): chi2={chi2_age:.4f}, dof={dof_age}, p={p_age:.4f}")

# Favorite genre row-wise % across gender
genre_by_gender_pct = (
    pd.crosstab(df["gender"], df["favorite_genre"], normalize="index") * 100
).round(2)
print("\nFavorite Genre Share (%) Within Each Gender Segment:")
print(genre_by_gender_pct.to_string())

# Chi-square test: gender vs. favorite_genre
ct_gen_genre = pd.crosstab(df["gender"], df["favorite_genre"])
chi2_gen, p_gen, dof_gen, _ = stats.chi2_contingency(ct_gen_genre)
print(f"\nChi-Square (gender vs favorite_genre): chi2={chi2_gen:.4f}, dof={dof_gen}, p={p_gen:.4f}")

# Top favorite genre per age group
top_genre_age = (
    genre_by_age_pct.idxmax(axis=1).to_frame(name="top_genre")
    .assign(top_share_pct=genre_by_age_pct.max(axis=1))
)
print("\nTop Favorite Genre per Age Group:")
print(top_genre_age.to_string())