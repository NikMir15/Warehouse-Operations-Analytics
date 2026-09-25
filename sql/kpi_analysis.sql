-- Executive KPI analysis

SELECT
    COUNT(*) AS records,
    SUM(units_picked) AS total_units_picked,
    SUM(orders_completed) AS total_orders_completed,
    ROUND(SUM(units_picked)::numeric / NULLIF(SUM(hours_worked), 0), 2) AS units_per_labour_hour,
    ROUND(
        100.0 * (SUM(units_picked) - SUM(picking_errors))
        / NULLIF(SUM(units_picked), 0),
        2
    ) AS picking_accuracy_pct,
    ROUND(
        100.0 * SUM(CASE WHEN order_processing_minutes <= sla_minutes THEN 1 ELSE 0 END)
        / COUNT(*),
        2
    ) AS sla_compliance_pct,
    ROUND(
        100.0 * SUM(orders_completed)
        / NULLIF(SUM(target_orders), 0),
        2
    ) AS target_achievement_pct,
    ROUND(SUM(overtime_hours), 2) AS total_overtime_hours
FROM warehouse_operations;
