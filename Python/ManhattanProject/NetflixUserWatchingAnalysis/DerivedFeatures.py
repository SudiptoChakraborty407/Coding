from pathlib import Path
import numpy as np
import pandas as pd

# ==============================================================================
# 1. LOAD DATASET
# ==============================================================================
BASE_DIR = Path(__file__).resolve().parent if "__file__" in globals() else Path(".")
df = pd.read_csv(BASE_DIR / "netflix_user_behavior_dataset.csv")


# ==============================================================================
# 2. ENGINEER DERIVED FEATURES
# ==============================================================================

# 1) Total Monthly Watch Time: estimated total watch minutes per 30-day month
df["total_monthly_watch_time"] = df["avg_watch_time_minutes"] * 30


# 2) Engagement Index: composite score of normalized content_interactions,
#    recommendation_click_rate, and rating_given (min-max scaled to [0, 1])
engagement_cols = [
    "content_interactions",
    "recommendation_click_rate",
    "rating_given",
]

norm_cols = []
for col in engagement_cols:
    col_min = df[col].min()
    col_max = df[col].max()
    norm_name = f"{col}_norm"
    if col_max > col_min:
        df[norm_name] = (df[col] - col_min) / (col_max - col_min)
    else:
        df[norm_name] = 0.0
    norm_cols.append(norm_name)

# Equal-weighted average (0.0 to 1.0 scale); multiply by 100 if you prefer a 0-100 index
df["engagement_index"] = df[norm_cols].mean(axis=1).round(4)

# Optional: drop temporary normalized helper columns if you only want the final index
df.drop(columns=norm_cols, inplace=True)


# 3) Tenure Cohorts: lifecycle segments based on account_age_months
#    New: < 6 months | Established: 6 to 24 months | Veteran: > 24 months
df["tenure_cohort"] = pd.cut(
    df["account_age_months"],
    bins=[-np.inf, 5, 24, np.inf],
    labels=["New (<6m)", "Established (6-24m)", "Veteran (>24m)"],
)


# 4) Watch Intensity per Session: avg_watch_time_minutes / watch_sessions_per_week
#    Safely guards against division by zero if watch_sessions_per_week is 0
df["watch_intensity_per_session"] = np.where(
    df["watch_sessions_per_week"] > 0,
    df["avg_watch_time_minutes"] / df["watch_sessions_per_week"],
    0.0,
).round(2)


# ==============================================================================
# 3. QUICK VERIFICATION & SUMMARY
# ==============================================================================
derived_cols = [
    "total_monthly_watch_time",
    "engagement_index",
    "tenure_cohort",
    "watch_intensity_per_session",
]

print(df[["user_id"] + derived_cols].head(5).to_string(index=False))
print("\nSummary statistics:")
print(df[derived_cols].describe(include="all").to_string())