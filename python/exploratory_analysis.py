from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "raw" / "warehouse_operations.csv"
OUTPUT_DIR = BASE_DIR / "screenshots"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# -------------------------------------------------------------------
# Load dataset
# -------------------------------------------------------------------

df = pd.read_csv(DATA_FILE, parse_dates=["order_date"])

print("Shape:", df.shape)
print("Missing values:", df.isna().sum().sum())


def productivity(data):
    return data["units_picked"].sum() / data["hours_worked"].sum()


def accuracy(data):
    return (
        1
        - data["picking_errors"].sum() / data["units_picked"].sum()
    ) * 100


# -------------------------------------------------------------------
# 1. Productivity by shift
# -------------------------------------------------------------------

shift_productivity = (
    df.groupby("shift")
    .apply(productivity, include_groups=False)
    .sort_values(ascending=False)
)

fig, ax = plt.subplots(figsize=(8, 5))

shift_productivity.plot(kind="bar", ax=ax)

ax.set_title("Warehouse Productivity by Shift")
ax.set_xlabel("Shift")
ax.set_ylabel("Units Picked per Labour Hour")
ax.tick_params(axis="x", rotation=0)

for i, value in enumerate(shift_productivity):
    ax.text(i, value + 0.05, f"{value:.2f}", ha="center")

plt.tight_layout()
plt.savefig(
    OUTPUT_DIR / "productivity_by_shift.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()


# -------------------------------------------------------------------
# 2. Picking accuracy by shift
# -------------------------------------------------------------------

shift_accuracy = (
    df.groupby("shift")
    .apply(accuracy, include_groups=False)
    .sort_values(ascending=False)
)

fig, ax = plt.subplots(figsize=(8, 5))

shift_accuracy.plot(kind="bar", ax=ax)

ax.set_title("Picking Accuracy by Shift")
ax.set_xlabel("Shift")
ax.set_ylabel("Picking Accuracy (%)")
ax.tick_params(axis="x", rotation=0)

ax.set_ylim(shift_accuracy.min() - 0.5, 100)

for i, value in enumerate(shift_accuracy):
    ax.text(i, value + 0.03, f"{value:.2f}%", ha="center")

plt.tight_layout()
plt.savefig(
    OUTPUT_DIR / "accuracy_by_shift.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()


# -------------------------------------------------------------------
# Night shift subset
# -------------------------------------------------------------------

night = df[df["shift"] == "Night"].copy()


# -------------------------------------------------------------------
# 3. Productivity by training status
# -------------------------------------------------------------------

training_productivity = (
    night.groupby("training_status")
    .apply(productivity, include_groups=False)
    .sort_values(ascending=False)
)

fig, ax = plt.subplots(figsize=(8, 5))

training_productivity.plot(kind="bar", ax=ax)

ax.set_title("Night Shift Productivity by Training Status")
ax.set_xlabel("Training Status")
ax.set_ylabel("Units Picked per Labour Hour")
ax.tick_params(axis="x", rotation=0)

for i, value in enumerate(training_productivity):
    ax.text(i, value + 0.05, f"{value:.2f}", ha="center")

plt.tight_layout()
plt.savefig(
    OUTPUT_DIR / "night_training_productivity.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()


# -------------------------------------------------------------------
# 4. Experience bands
# -------------------------------------------------------------------

experience_bins = [0, 12, 24, 48, float("inf")]

experience_labels = [
    "0-11 months",
    "12-23 months",
    "24-47 months",
    "48+ months"
]

night["experience_band"] = pd.cut(
    night["experience_months"],
    bins=experience_bins,
    labels=experience_labels,
    right=False
)


# -------------------------------------------------------------------
# 5. Productivity by experience
# -------------------------------------------------------------------

experience_productivity = (
    night.groupby("experience_band", observed=True)
    .apply(productivity, include_groups=False)
)

fig, ax = plt.subplots(figsize=(9, 5))

experience_productivity.plot(kind="bar", ax=ax)

ax.set_title("Night Shift Productivity by Experience")
ax.set_xlabel("Experience Band")
ax.set_ylabel("Units Picked per Labour Hour")
ax.tick_params(axis="x", rotation=0)

for i, value in enumerate(experience_productivity):
    ax.text(i, value + 0.05, f"{value:.2f}", ha="center")

plt.tight_layout()
plt.savefig(
    OUTPUT_DIR / "night_productivity_by_experience.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()


# -------------------------------------------------------------------
# 6. Training status by experience
# -------------------------------------------------------------------

training_experience = (
    night.groupby(
        ["experience_band", "training_status"],
        observed=True
    )
    .apply(productivity, include_groups=False)
    .unstack()
)

fig, ax = plt.subplots(figsize=(10, 6))

training_experience.plot(kind="bar", ax=ax)

ax.set_title("Night Shift Productivity: Training by Experience")
ax.set_xlabel("Experience Band")
ax.set_ylabel("Units Picked per Labour Hour")
ax.tick_params(axis="x", rotation=0)
ax.legend(title="Training Status")

plt.tight_layout()
plt.savefig(
    OUTPUT_DIR / "training_by_experience.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()


# -------------------------------------------------------------------
# 7. Experience vs productivity scatter plot
# -------------------------------------------------------------------

employee_summary = (
    night.groupby("employee_id")
    .agg(
        experience_months=("experience_months", "mean"),
        units_picked=("units_picked", "sum"),
        hours_worked=("hours_worked", "sum")
    )
)

employee_summary["productivity"] = (
    employee_summary["units_picked"]
    / employee_summary["hours_worked"]
)

fig, ax = plt.subplots(figsize=(9, 6))

ax.scatter(
    employee_summary["experience_months"],
    employee_summary["productivity"],
    alpha=0.6
)

ax.set_title("Night Shift: Experience vs Productivity")
ax.set_xlabel("Experience (Months)")
ax.set_ylabel("Units Picked per Labour Hour")

plt.tight_layout()
plt.savefig(
    OUTPUT_DIR / "experience_vs_productivity.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()


# -------------------------------------------------------------------
# Console summary
# -------------------------------------------------------------------

print("\nEDA complete.")

print("\nShift productivity:")
print(shift_productivity.round(2))

print("\nShift accuracy:")
print(shift_accuracy.round(2))

print("\nNight-shift productivity by training:")
print(training_productivity.round(2))

print("\nNight-shift productivity by experience:")
print(experience_productivity.round(2))

print(f"\nCharts saved to: {OUTPUT_DIR}")
