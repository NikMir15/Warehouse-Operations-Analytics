-- Performance by shift

SELECT
    shift,
    SUM(units_picked) AS units_picked,
    ROUND(SUM(units_picked)::numeric / NULLIF(SUM(hours_worked), 0), 2) AS productivity,
    ROUND(
        100.0 * SUM(picking_errors) / NULLIF(SUM(units_picked), 0),
        2
    ) AS error_rate_pct,
    ROUND(SUM(overtime_hours), 2) AS overtime_hours,
    ROUND(
        100.0 * SUM(CASE WHEN order_processing_minutes <= sla_minutes THEN 1 ELSE 0 END)
        / COUNT(*),
        2
    ) AS sla_compliance_pct
FROM warehouse_operations
GROUP BY shift
ORDER BY productivity DESC;
