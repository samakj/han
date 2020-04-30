CREATE_DEVICE_REPORT_METRIC_QUERY = """
INSERT INTO device_report_metrics (device_report_metric_id, device_id, report_metric_id)
     VALUES (:device_report_metric_id, :device_id, :report_metric_id)
  RETURNING device_report_metric_id, device_id, report_metric_id
"""

GET_DEVICE_REPORT_METRIC_QUERY_TEMPLATE = """
SELECT {fields}
  FROM device_report_metrics
 WHERE device_report_metric_id = :device_report_metric_id 
"""

GET_DEVICE_REPORT_METRICS_QUERY_TEMPLATE = """
  SELECT {fields}
    FROM device_report_metrics
   WHERE {where_conditions}
ORDER BY {order_by_condition}
"""

UPDATE_DEVICE_REPORT_METRIC_QUERY = """
   UPDATE device_report_metrics
      SET {set_conditions}
    WHERE device_report_metric_id = :device_report_metric_id
RETURNING device_report_metric_id, device_id, report_metric_id
"""

DELETE_DEVICE_REPORT_METRIC_QUERY = """
DELETE FROM device_report_metrics
      WHERE device_report_metric_id = :device_report_metric_id
  RETURNING :device_report_metric_id
"""
