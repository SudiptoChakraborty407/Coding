from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

# ==============================================================================
# 0. LOAD & PREPARE DATA
# ==============================================================================
BASE_DIR = Path(__file__).resolve().parent if "__file__" in globals() else Path(".")
df = pd.read_csv(BASE_DIR / "netflix_user_behavior_dataset.csv")

# Binary churn indicator: 1 = churned ('Yes'), 0 = active/retained ('No')
df["churn_flag"] = (
    df["churned"].astype(str).str.strip().str.lower() == "yes"
).astype(int)

# Lifecycle tenure cohorts (matching Recommended Derived Features)
df["tenure_cohort"] = pd.cut(
    df["account_age_months"],
    bins=[-np.inf, 5, 24, np.inf],
    labels=["New (<6m)", "Established (6-24m)", "Veteran (>24m)"],
)

# Recency buckets based on days_since_last_login
df["recency_bucket"] = pd.cut(
    df["days_since_last_login"],
    bins=[-1, 7, 14, 30, 45, np.inf],
    labels=["0-7d", "8-14d", "15-30d", "31-45d", "46d+"],
)


# ==============================================================================
# 4.1 TENURE-BASED CHURN CURVES
# Identify account_age_months milestones where churn is most heavily concentrated
# ==============================================================================
print("\n" + "=" * 80)
print("4.1 TENURE-BASED CHURN CURVES (BY ACCOUNT_AGE_MONTHS & COHORT)")
print("=" * 80)

tenure_curve = (
    df.groupby("account_age_months", observed=False)
    .agg(
        total_users=("user_id", "count"),
        churned_users=("churn_flag", "sum"),
        churn_rate_pct=("churn_flag", lambda s: round(s.mean() * 100, 2)),
        retention_rate_pct=("churn_flag", lambda s: round((1 - s.mean()) * 100, 2)),
    )
    .reset_index()
)

total_churned = df["churn_flag"].sum()
tenure_curve["share_of_all_churn_pct"] = (
    tenure_curve["churned_users"] / total_churned * 100
).round(2)
tenure_curve["cumulative_churn_share_pct"] = (
    tenure_curve["share_of_all_churn_pct"].cumsum().round(2)
)

print("Churn Curve Across Tenure Milestones (Sample / Key Months):")
print(tenure_curve.to_string(index=False))

peak_rate_row = tenure_curve.loc[tenure_curve["churn_rate_pct"].idxmax()]
peak_vol_row = tenure_curve.loc[tenure_curve["churned_users"].idxmax()]
print(
    f"\nHighest Churn Rate Milestone: Month {int(peak_rate_row['account_age_months'])} "
    f"({peak_rate_row['churn_rate_pct']:.2f}% churn across {int(peak_rate_row['total_users'])} users)"
)
print(
    f"Highest Churned User Volume Milestone: Month {int(peak_vol_row['account_age_months'])} "
    f"({int(peak_vol_row['churned_users'])} churned users, {peak_vol_row['share_of_all_churn_pct']:.2f}% of all churn)"
)

# Cohort-level summary
cohort_churn = (
    df.groupby("tenure_cohort", observed=False)
    .agg(
        users=("user_id", "count"),
        churned_users=("churn_flag", "sum"),
        churn_rate_pct=("churn_flag", lambda s: round(s.mean() * 100, 2)),
        share_of_all_churn_pct=("churn_flag", lambda s: round(s.sum() / total_churned * 100, 2)),
    )
)
print("\nChurn Summary by Tenure Cohort:")
print(cohort_churn.to_string())


# ==============================================================================
# 4.2 ENGAGEMENT DECAY OVER TIME
# Track avg_watch_time_minutes, recommendation_click_rate, content_interactions
# ==============================================================================
print("\n" + "=" * 80)
print("4.2 ENGAGEMENT DECAY OVER ACCOUNT TENURE")
print("=" * 80)

engagement_metrics = [
    "avg_watch_time_minutes",
    "recommendation_click_rate",
    "content_interactions",
]

decay_by_cohort = (
    df.groupby("tenure_cohort", observed=False)[engagement_metrics]
    .agg(["mean", "median", "std"])
    .round(2)
)
print("Engagement Metrics by Tenure Cohort:")
print(decay_by_cohort.to_string())

decay_by_month = (
    df.groupby("account_age_months", observed=False)[engagement_metrics]
    .mean()
    .round(2)
    .reset_index()
)
print("\nMonthly Mean Engagement Trajectory (First 15 Months):")
print(decay_by_month.head(15).to_string(index=False))

# Linear trend / fatigue check (OLS slope & correlation with account_age_months)
print("\nEngagement Fatigue Check (Linear Trend vs. account_age_months):")
for metric in engagement_metrics:
    corr_val = df["account_age_months"].corr(df[metric])
    ols_model = smf.ols(f"{metric} ~ account_age_months", data=df).fit()
    slope = ols_model.params["account_age_months"]
    p_val = ols_model.pvalues["account_age_months"]
    print(
        f"  {metric:26s} | r={corr_val:+.4f} | slope={slope:+.4f}/month | p={p_val:.4f}"
    )


# ==============================================================================
# 4.3 RECENCY VS. TENURE RISK
# Interaction of days_since_last_login and account_age_months on imminent churn
# ==============================================================================
print("\n" + "=" * 80)
print("4.3 RECENCY VS. TENURE INTERACTION ON CHURN RISK")
print("=" * 80)

# Churn rate matrix: Tenure Cohort x Recency Bucket
recency_tenure_churn = df.pivot_table(
    index="tenure_cohort",
    columns="recency_bucket",
    values="churn_flag",
    aggfunc=lambda s: round(s.mean() * 100, 2),
    observed=False,
)
print("Churn Rate (%) Matrix — Tenure Cohort (rows) x Days Since Last Login (columns):")
print(recency_tenure_churn.to_string())

# User counts in each Tenure Cohort x Recency Bucket cell
recency_tenure_counts = df.pivot_table(
    index="tenure_cohort",
    columns="recency_bucket",
    values="user_id",
    aggfunc="count",
    observed=False,
)
print("\nUser Count Matrix — Tenure Cohort x Days Since Last Login:")
print(recency_tenure_counts.to_string())