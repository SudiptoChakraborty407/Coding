from pathlib import Path
import numpy as np
import pandas as pd

# ==============================================================================
# 0. LOAD DATASET
# ==============================================================================
BASE_DIR = Path(__file__).resolve().parent if "__file__" in globals() else Path(".")
df = pd.read_csv(BASE_DIR / "netflix_user_behavior_dataset.csv")

print(f"Dataset shape: {df.shape[0]:,} users x {df.shape[1]} columns")


# ==============================================================================
# 1. PLATFORM CHURN BASELINE
# ==============================================================================
print("\n" + "=" * 75)
print("1. PLATFORM CHURN BASELINE")
print("=" * 75)

churn_counts = df["churned"].value_counts(dropna=False)
churn_pct = df["churned"].value_counts(normalize=True, dropna=False) * 100

churn_summary = pd.DataFrame({
    "user_count": churn_counts,
    "share_pct": churn_pct.round(2),
})
print(churn_summary.to_string())

canceled_rate = (df["churned"].astype(str).str.strip().str.lower() == "yes").mean() * 100
print(f"\nOverall platform churn rate (actively canceled): {canceled_rate:.2f}%")


# ==============================================================================
# 2. SUBSCRIPTION TIER DISTRIBUTION & REVENUE SHARE
# ==============================================================================
print("\n" + "=" * 75)
print("2. SUBSCRIPTION TIER DISTRIBUTION & MONTHLY REVENUE")
print("=" * 75)

tier_order = ["Basic", "Standard", "Premium"]
tier_summary = (
    df.groupby("subscription_type", observed=False)
    .agg(
        users=("user_id", "count"),
        avg_monthly_fee=("monthly_fee", "mean"),
        total_monthly_revenue=("monthly_fee", "sum"),
    )
    .reindex(tier_order)
)

total_users = tier_summary["users"].sum()
total_revenue = tier_summary["total_monthly_revenue"].sum()

tier_summary["user_share_pct"] = (tier_summary["users"] / total_users * 100).round(2)
tier_summary["revenue_share_pct"] = (
    tier_summary["total_monthly_revenue"] / total_revenue * 100
).round(2)
tier_summary["avg_monthly_fee"] = tier_summary["avg_monthly_fee"].round(2)
tier_summary["total_monthly_revenue"] = tier_summary["total_monthly_revenue"].round(2)

print(
    tier_summary[
        ["users", "user_share_pct", "avg_monthly_fee", "total_monthly_revenue", "revenue_share_pct"]
    ].to_string()
)
print(f"\nTotal Estimated Monthly Fee Revenue (all 50,000 users): ${total_revenue:,.2f}")


# ==============================================================================
# 3. ENGAGEMENT SPREAD: WATCH TIME & BINGE WATCH SESSIONS
# ==============================================================================
print("\n" + "=" * 75)
print("3. ENGAGEMENT SPREAD (WATCH TIME & BINGE SESSIONS)")
print("=" * 75)

eng_cols = ["avg_watch_time_minutes", "binge_watch_sessions"]
eng_stats = df[eng_cols].describe(percentiles=[0.1, 0.25, 0.5, 0.75, 0.9]).T
eng_stats["skewness"] = df[eng_cols].skew().round(3)
print(eng_stats.round(2).to_string())

# Casual vs. Moderate vs. Heavy Binge-Watchers (binge_watch_sessions ranges 0-14)
binge_segments = pd.cut(
    df["binge_watch_sessions"],
    bins=[-1, 2, 7, np.inf],
    labels=["Casual / Low Binge (0-2)", "Moderate Binge (3-7)", "Heavy Binge (8+)"],
)
binge_dist = pd.DataFrame({
    "users": binge_segments.value_counts(),
    "share_pct": (binge_segments.value_counts(normalize=True) * 100).round(2),
})
print("\nBinge-Watching Habit Breakdown:")
print(binge_dist.to_string())

# Daily Watch Time tiers (avg_watch_time_minutes ranges 10-299)
watch_segments = pd.cut(
    df["avg_watch_time_minutes"],
    bins=[0, 60, 180, np.inf],
    labels=["Light (<60 min/day)", "Moderate (60-180 min/day)", "Heavy (>180 min/day)"],
)
watch_dist = pd.DataFrame({
    "users": watch_segments.value_counts(),
    "share_pct": (watch_segments.value_counts(normalize=True) * 100).round(2),
})
print("\nDaily Watch Time Breakdown:")
print(watch_dist.to_string())


# ==============================================================================
# 4. DORMANCY LEVELS (DAYS SINCE LAST LOGIN)
# ==============================================================================
print("\n" + "=" * 75)
print("4. DORMANCY LEVELS (DAYS SINCE LAST LOGIN)")
print("=" * 75)

login_stats = df["days_since_last_login"].describe(percentiles=[0.1, 0.25, 0.5, 0.75, 0.9])
print(login_stats.round(2).to_string())

# Recency / Risk buckets (days_since_last_login ranges 0-59)
dormancy_buckets = pd.cut(
    df["days_since_last_login"],
    bins=[-1, 14, 30, 45, np.inf],
    labels=[
        "Active / Recent (0-14d)",
        "Cooling / Watchlist (15-30d)",
        "At-Risk / Dormant (31-45d)",
        "High-Dormancy / Lapsed (46d+)",
    ],
)
dormancy_dist = pd.DataFrame({
    "users": dormancy_buckets.value_counts(),
    "share_pct": (dormancy_buckets.value_counts(normalize=True) * 100).round(2),
})
print("\nDormancy & Drop-Off Risk Breakdown:")
print(dormancy_dist.to_string())

at_risk_30plus = (df["days_since_last_login"] > 30).mean() * 100
dormant_45plus = (df["days_since_last_login"] > 45).mean() * 100
print(f"\nUsers inactive > 30 days: {at_risk_30plus:.2f}% | Users inactive > 45 days: {dormant_45plus:.2f}%")


# ==============================================================================
# 5. DEMOGRAPHIC REACH: COUNTRY, AGE & PRIMARY DEVICE
# ==============================================================================
print("\n" + "=" * 75)
print("5. DEMOGRAPHIC REACH (COUNTRY, AGE & PRIMARY DEVICE)")
print("=" * 75)

# 5a. Country
country_dist = pd.DataFrame({
    "users": df["country"].value_counts(),
    "share_pct": (df["country"].value_counts(normalize=True) * 100).round(2),
})
print("\nCountry Distribution:")
print(country_dist.to_string())

# 5b. Age summary & age brackets
print("\nAge Summary Statistics:")
print(df["age"].describe().round(2).to_string())

age_groups = pd.cut(
    df["age"],
    bins=[0, 24, 34, 44, 54, np.inf],
    labels=["18-24", "25-34", "35-44", "45-54", "55+"],
)
age_dist = pd.DataFrame({
    "users": age_groups.value_counts(),
    "share_pct": (age_groups.value_counts(normalize=True) * 100).round(2),
})
print("\nAge Bracket Distribution:")
print(age_dist.to_string())

# 5c. Primary Device
device_dist = pd.DataFrame({
    "users": df["primary_device"].value_counts(),
    "share_pct": (df["primary_device"].value_counts(normalize=True) * 100).round(2),
})
print("\nPrimary Device Distribution:")
print(device_dist.to_string())