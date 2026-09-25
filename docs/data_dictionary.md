# Data Dictionary

| Column | Type | Description |
|---|---|---|
| order_id | text | Unique warehouse order identifier |
| order_date | date | Date the warehouse activity occurred |
| shift | text | Morning, Afternoon, or Night shift |
| warehouse_zone | text | Operational warehouse zone |
| employee_id | text | Synthetic employee identifier |
| team | text | Operational team assigned to the employee |
| product_category | text | Product category handled |
| units_picked | integer | Number of units picked |
| hours_worked | decimal | Labour hours worked |
| picking_errors | integer | Number of picking errors recorded |
| orders_completed | integer | Number of orders completed |
| target_orders | integer | Expected order target |
| overtime_hours | decimal | Overtime hours worked |
| training_status | text | Whether required training was completed |
| experience_months | integer | Employee experience in months |
| order_processing_minutes | decimal | Average processing time for the record |
| sla_minutes | integer | Maximum target processing time |
| absence_flag | integer | 1 if absence affected the operational period, otherwise 0 |
