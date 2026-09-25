from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "raw" / "warehouse_operations.csv"
OUTPUT_FILE = BASE_DIR / "data" / "processed" / "warehouse_operations_powerbi.csv"


def main():

    df = pd.read_csv(INPUT_FILE)

    # ---------------------------------------------------------
    # Date preparation
    # ---------------------------------------------------------

    df["order_date"] = pd.to_datetime(df["order_date"])

    df["year"] = df["order_date"].dt.year
    df["month"] = df["order_date"].dt.month_name()
    df["month_number"] = df["order_date"].dt.month
    df["year_month"] = df["order_date"].dt.to_period("M").astype(str)
    df["day_of_week"] = df["order_date"].dt.day_name()

    # ---------------------------------------------------------
    # Experience bands
    # ---------------------------------------------------------

    df["experience_band"] = pd.cut(
        df["experience_months"],
        bins=[0, 12, 24, 48, float("inf")],
        labels=[
            "0-11 months",
            "12-23 months",
            "24-47 months",
            "48+ months"
        ],
        right=False
    )

    # ---------------------------------------------------------
    # SLA performance
    # ---------------------------------------------------------

    df["sla_status"] = df.apply(
        lambda row: (
            "Within SLA"
            if row["order_processing_minutes"] <= row["sla_minutes"]
            else "SLA Missed"
        ),
        axis=1
    )

    # ---------------------------------------------------------
    # Target performance
    # ---------------------------------------------------------

    df["target_status"] = df.apply(
        lambda row: (
            "Target Met"
            if row["orders_completed"] >= row["target_orders"]
            else "Target Missed"
        ),
        axis=1
    )

    # ---------------------------------------------------------
    # Row-level helper fields
    # ---------------------------------------------------------

    df["productivity_per_hour"] = (
        df["units_picked"] / df["hours_worked"]
    ).round(2)

    df["error_rate_pct"] = (
        df["picking_errors"]
        / df["units_picked"]
        * 100
    ).round(2)

    df["target_achievement_pct"] = (
        df["orders_completed"]
        / df["target_orders"]
        * 100
    ).round(2)

    # ---------------------------------------------------------
    # Save processed dataset
    # ---------------------------------------------------------

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("Power BI dataset created successfully.")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")
    print(f"Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
