CREATE TABLE IF NOT EXISTS warehouse_operations (
    order_id VARCHAR(20) PRIMARY KEY,
    order_date DATE NOT NULL,
    shift VARCHAR(20) NOT NULL,
    warehouse_zone VARCHAR(20) NOT NULL,
    employee_id VARCHAR(20) NOT NULL,
    team VARCHAR(20) NOT NULL,
    product_category VARCHAR(50) NOT NULL,
    units_picked INTEGER NOT NULL,
    hours_worked NUMERIC(5,2) NOT NULL,
    picking_errors INTEGER NOT NULL,
    orders_completed INTEGER NOT NULL,
    target_orders INTEGER NOT NULL,
    overtime_hours NUMERIC(5,2) NOT NULL,
    training_status VARCHAR(20) NOT NULL,
    experience_months INTEGER NOT NULL,
    order_processing_minutes NUMERIC(8,2) NOT NULL,
    sla_minutes INTEGER NOT NULL,
    absence_flag INTEGER NOT NULL CHECK (absence_flag IN (0,1))
);

CREATE INDEX IF NOT EXISTS idx_warehouse_order_date
ON warehouse_operations(order_date);

CREATE INDEX IF NOT EXISTS idx_warehouse_shift
ON warehouse_operations(shift);

CREATE INDEX IF NOT EXISTS idx_warehouse_employee
ON warehouse_operations(employee_id);
