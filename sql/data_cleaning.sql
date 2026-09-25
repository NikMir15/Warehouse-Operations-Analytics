-- Basic data-quality checks

SELECT COUNT(*) AS total_rows
FROM warehouse_operations;

SELECT COUNT(*) AS rows_with_invalid_hours
FROM warehouse_operations
WHERE hours_worked <= 0;

SELECT COUNT(*) AS rows_with_negative_values
FROM warehouse_operations
WHERE units_picked < 0
   OR picking_errors < 0
   OR orders_completed < 0
   OR overtime_hours < 0;

SELECT order_id, COUNT(*)
FROM warehouse_operations
GROUP BY order_id
HAVING COUNT(*) > 1;
