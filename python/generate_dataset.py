from pathlib import Path
import numpy as np
import pandas as pd

RNG = np.random.default_rng(42)
ROWS = 50000
OUTPUT = Path(__file__).resolve().parents[1] / "data" / "raw" / "warehouse_operations.csv"


def generate_dataset(rows: int = ROWS) -> pd.DataFrame:
    dates = pd.date_range("2025-01-01", "2025-12-31", freq="D")
    shifts = np.array(["Morning", "Afternoon", "Night"])
    zones = np.array(["Zone A", "Zone B", "Zone C", "Zone D"])
    teams = np.array(["Team 1", "Team 2", "Team 3", "Team 4"])
    categories = np.array(["Footwear", "Clothing", "Accessories", "Sports", "Home"])

    employee_numbers = RNG.integers(1, 251, rows)
    employee_ids = np.array([f"EMP-{n:03d}" for n in employee_numbers])

    order_dates = RNG.choice(dates, rows)
    shift = RNG.choice(shifts, rows, p=[0.40, 0.35, 0.25])
    zone = RNG.choice(zones, rows)
    team = RNG.choice(teams, rows)
    category = RNG.choice(categories, rows)

    experience_months = RNG.integers(1, 73, rows)
    training_probability = np.clip(0.70 + (experience_months / 300), 0.70, 0.94)
    trained = RNG.random(rows) < training_probability
    training_status = np.where(trained, "Completed", "Pending")

    hours_worked = np.round(RNG.normal(7.6, 0.7, rows), 2)
    hours_worked = np.clip(hours_worked, 4.0, 10.0)

    base_productivity = RNG.normal(11.5, 1.4, rows)
    shift_effect = np.select(
        [shift == "Morning", shift == "Afternoon", shift == "Night"],
        [0.8, 0.2, -0.7],
        default=0,
    )
    training_effect = np.where(trained, 0.7, -0.4)
    experience_effect = np.minimum(experience_months / 30, 1.5)

    month = pd.DatetimeIndex(order_dates).month.to_numpy()
    peak_effect = np.where(np.isin(month, [11, 12]), 1.4, 0.0)

    units_picked = np.round(
        hours_worked
        * (base_productivity + shift_effect + training_effect + experience_effect + peak_effect)
    ).astype(int)
    units_picked = np.clip(units_picked, 15, None)

    base_error_rate = 0.018
    error_rate = (
        base_error_rate
        + np.where(shift == "Night", 0.008, 0)
        + np.where(~trained, 0.010, 0)
        + np.where(experience_months < 6, 0.008, 0)
        + np.where(np.isin(month, [11, 12]), 0.005, 0)
    )
    picking_errors = RNG.binomial(units_picked, np.clip(error_rate, 0.005, 0.08))

    orders_completed = np.maximum(1, np.round(units_picked / RNG.uniform(2.3, 3.3, rows))).astype(int)
    target_orders = np.maximum(1, np.round(hours_worked * RNG.uniform(4.3, 5.2, rows))).astype(int)

    overtime_hours = np.where(
        np.isin(month, [11, 12]),
        RNG.gamma(1.8, 0.45, rows),
        RNG.gamma(0.7, 0.25, rows),
    )
    overtime_hours = np.round(np.clip(overtime_hours, 0, 4), 2)

    workload_factor = units_picked / np.maximum(hours_worked, 1)
    processing_minutes = (
        RNG.normal(20, 3.5, rows)
        + np.where(shift == "Night", 2.2, 0)
        + np.where(workload_factor > 14, 2.5, 0)
        + np.where(~trained, 1.8, 0)
        + np.where(np.isin(month, [11, 12]), 2.0, 0)
    )
    processing_minutes = np.round(np.clip(processing_minutes, 7, 50), 2)

    sla_minutes = RNG.choice([20, 25, 30], rows, p=[0.25, 0.55, 0.20])
    absence_flag = RNG.binomial(1, 0.035, rows)

    df = pd.DataFrame({
        "order_id": [f"ORD-{i:06d}" for i in range(1, rows + 1)],
        "order_date": pd.to_datetime(order_dates),
        "shift": shift,
        "warehouse_zone": zone,
        "employee_id": employee_ids,
        "team": team,
        "product_category": category,
        "units_picked": units_picked,
        "hours_worked": hours_worked,
        "picking_errors": picking_errors,
        "orders_completed": orders_completed,
        "target_orders": target_orders,
        "overtime_hours": overtime_hours,
        "training_status": training_status,
        "experience_months": experience_months,
        "order_processing_minutes": processing_minutes,
        "sla_minutes": sla_minutes,
        "absence_flag": absence_flag,
    })

    return df.sort_values("order_date").reset_index(drop=True)


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    df = generate_dataset()
    df.to_csv(OUTPUT, index=False)
    print(f"Generated {len(df):,} rows")
    print(f"Saved to: {OUTPUT}")
    print(df.head())


if __name__ == "__main__":
    main()
