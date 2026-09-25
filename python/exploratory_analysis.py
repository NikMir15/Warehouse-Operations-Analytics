from pathlib import Path
import pandas as pd

DATA = Path(__file__).resolve().parents[1] / "data" / "raw" / "warehouse_operations.csv"


def main() -> None:
    df = pd.read_csv(DATA, parse_dates=["order_date"])

    print("Shape:", df.shape)
    print("\nMissing values:\n", df.isna().sum())

    productivity = df["units_picked"].sum() / df["hours_worked"].sum()
    accuracy = 100 * (df["units_picked"].sum() - df["picking_errors"].sum()) / df["units_picked"].sum()

    print(f"\nOverall productivity: {productivity:.2f} units/hour")
    print(f"Overall picking accuracy: {accuracy:.2f}%")

    shift_summary = (
        df.groupby("shift")
        .agg(
            units_picked=("units_picked", "sum"),
            hours_worked=("hours_worked", "sum"),
            picking_errors=("picking_errors", "sum"),
            overtime_hours=("overtime_hours", "sum"),
        )
    )
    shift_summary["productivity"] = shift_summary["units_picked"] / shift_summary["hours_worked"]
    shift_summary["error_rate_pct"] = 100 * shift_summary["picking_errors"] / shift_summary["units_picked"]

    print("\nShift summary:\n", shift_summary.round(2))


if __name__ == "__main__":
    main()
