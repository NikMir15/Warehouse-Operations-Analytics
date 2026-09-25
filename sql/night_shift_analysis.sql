/*
===============================================================================
Warehouse Operations Analytics
Night Shift Analysis
===============================================================================

Purpose:
Analyse Night-shift performance across:
1. Training status
2. Warehouse zone
3. Experience band
4. Training status within each experience band

Key KPIs:
- Productivity = total units picked / total hours worked
- Picking accuracy = 1 - (picking errors / units picked)
- Average processing time

Notes:
- This project uses synthetic warehouse data.
- Results show associations, not causal relationships.
===============================================================================
*/


/* ============================================================================
1. NIGHT SHIFT PERFORMANCE BY TRAINING STATUS
===============================================================================

Business question:
Do employees with completed training perform differently from employees whose
training is still pending?

Expected interpretation:
Compare productivity, picking accuracy, and processing time between training
groups.
============================================================================ */

SELECT
    training_status,
    COUNT(*) AS records,

    ROUND(
        SUM(units_picked)::numeric / NULLIF(SUM(hours_worked), 0),
        2
    ) AS productivity_units_per_hour,

    ROUND(
        (
            1
            - SUM(picking_errors)::numeric
              / NULLIF(SUM(units_picked), 0)
        ) * 100,
        2
    ) AS picking_accuracy_pct,

    ROUND(
        AVG(order_processing_minutes)::numeric,
        2
    ) AS avg_processing_minutes

FROM warehouse_operations

WHERE shift = 'Night'

GROUP BY training_status

ORDER BY productivity_units_per_hour DESC;


/* ============================================================================
2. NIGHT SHIFT PERFORMANCE BY WAREHOUSE ZONE
===============================================================================

Business question:
Is one warehouse zone responsible for weaker Night-shift performance?

Expected interpretation:
If performance is broadly similar across zones, zone allocation is unlikely to
be the primary explanation for Night-shift underperformance.
============================================================================ */

SELECT
    warehouse_zone,
    COUNT(*) AS records,

    ROUND(
        SUM(units_picked)::numeric / NULLIF(SUM(hours_worked), 0),
        2
    ) AS productivity_units_per_hour,

    ROUND(
        (
            1
            - SUM(picking_errors)::numeric
              / NULLIF(SUM(units_picked), 0)
        ) * 100,
        2
    ) AS picking_accuracy_pct,

    ROUND(
        AVG(order_processing_minutes)::numeric,
        2
    ) AS avg_processing_minutes

FROM warehouse_operations

WHERE shift = 'Night'

GROUP BY warehouse_zone

ORDER BY productivity_units_per_hour ASC;


/* ============================================================================
3. NIGHT SHIFT PERFORMANCE BY EXPERIENCE BAND
===============================================================================

Business question:
Does employee experience appear to be associated with Night-shift performance?

Experience bands:
- 0–11 months
- 12–23 months
- 24–47 months
- 48+ months

Expected interpretation:
Look for changes in productivity and accuracy as workforce experience increases.
============================================================================ */

SELECT
    CASE
        WHEN experience_months < 12 THEN '0-11 months'
        WHEN experience_months < 24 THEN '12-23 months'
        WHEN experience_months < 48 THEN '24-47 months'
        ELSE '48+ months'
    END AS experience_band,

    COUNT(*) AS records,

    ROUND(
        SUM(units_picked)::numeric / NULLIF(SUM(hours_worked), 0),
        2
    ) AS productivity_units_per_hour,

    ROUND(
        (
            1
            - SUM(picking_errors)::numeric
              / NULLIF(SUM(units_picked), 0)
        ) * 100,
        2
    ) AS picking_accuracy_pct,

    ROUND(
        AVG(order_processing_minutes)::numeric,
        2
    ) AS avg_processing_minutes

FROM warehouse_operations

WHERE shift = 'Night'

GROUP BY
    CASE
        WHEN experience_months < 12 THEN '0-11 months'
        WHEN experience_months < 24 THEN '12-23 months'
        WHEN experience_months < 48 THEN '24-47 months'
        ELSE '48+ months'
    END

ORDER BY MIN(experience_months);


/* ============================================================================
4. TRAINING STATUS WITHIN EACH EXPERIENCE BAND
===============================================================================

Business question:
Does training status still appear to matter after controlling for experience
level?

Why this matters:
Training and experience may overlap. This analysis compares Completed and
Pending training within the same experience bands to reduce that confounding.

Expected interpretation:
If Completed employees outperform Pending employees within each experience band,
training status is associated with performance beyond experience alone.
============================================================================ */

SELECT
    CASE
        WHEN experience_months < 12 THEN '0-11 months'
        WHEN experience_months < 24 THEN '12-23 months'
        WHEN experience_months < 48 THEN '24-47 months'
        ELSE '48+ months'
    END AS experience_band,

    training_status,

    COUNT(*) AS records,

    ROUND(
        SUM(units_picked)::numeric / NULLIF(SUM(hours_worked), 0),
        2
    ) AS productivity_units_per_hour,

    ROUND(
        (
            1
            - SUM(picking_errors)::numeric
              / NULLIF(SUM(units_picked), 0)
        ) * 100,
        2
    ) AS picking_accuracy_pct,

    ROUND(
        AVG(order_processing_minutes)::numeric,
        2
    ) AS avg_processing_minutes

FROM warehouse_operations

WHERE shift = 'Night'

GROUP BY
    CASE
        WHEN experience_months < 12 THEN '0-11 months'
        WHEN experience_months < 24 THEN '12-23 months'
        WHEN experience_months < 48 THEN '24-47 months'
        ELSE '48+ months'
    END,
    training_status

ORDER BY
    MIN(experience_months),
    training_status;


/* ============================================================================
5. SUMMARY CHECK
===============================================================================

Optional final query:
Provides the overall Night-shift baseline for comparison with the segmented
analyses above.
============================================================================ */

SELECT
    COUNT(*) AS night_shift_records,

    ROUND(
        SUM(units_picked)::numeric / NULLIF(SUM(hours_worked), 0),
        2
    ) AS productivity_units_per_hour,

    ROUND(
        (
            1
            - SUM(picking_errors)::numeric
              / NULLIF(SUM(units_picked), 0)
        ) * 100,
        2
    ) AS picking_accuracy_pct,

    ROUND(
        AVG(order_processing_minutes)::numeric,
        2
    ) AS avg_processing_minutes,

    ROUND(
        SUM(overtime_hours)::numeric,
        2
    ) AS total_overtime_hours

FROM warehouse_operations

WHERE shift = 'Night';
