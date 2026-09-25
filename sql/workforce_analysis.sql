-- Training and workforce performance

SELECT
    training_status,
    COUNT(DISTINCT employee_id) AS employees,
    ROUND(SUM(units_picked)::numeric / NULLIF(SUM(hours_worked), 0), 2) AS productivity,
    ROUND(
        100.0 * SUM(picking_errors) / NULLIF(SUM(units_picked), 0),
        2
    ) AS error_rate_pct,
    ROUND(
        100.0 * SUM(orders_completed) / NULLIF(SUM(target_orders), 0),
        2
    ) AS target_achievement_pct
FROM warehouse_operations
GROUP BY training_status
ORDER BY productivity DESC;
