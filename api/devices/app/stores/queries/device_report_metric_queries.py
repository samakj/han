import os

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

BACKUP_DEVICE_REPORT_METRICS = f"""
     COPY device_report_metrics 
       TO '{os.environ.get("POSTGRES_BACKUP") or '/backup'}/device_report_metrics.csv' 
DELIMITER ',' 
      CSV 
   HEADER;
"""

LOAD_DEVICE_REPORT_METRICS_FROM_BACKUP = f"""
CREATE TABLE _device_report_metrics (LIKE device_report_metrics INCLUDING DEFAULTS);

     COPY _device_report_metrics
     FROM '{os.environ.get("POSTGRES_BACKUP") or '/backup'}/device_report_metrics.csv'
DELIMITER ',' 
      CSV 
   HEADER;

INSERT INTO device_report_metrics
     SELECT *
       FROM _device_report_metrics
ON CONFLICT
         DO NOTHING;

DROP TABLE _device_report_metrics;

SELECT setval(
       pg_get_serial_sequence('device_report_metrics','device_report_metric_id'), 
       (SELECT MAX(device_report_metric_id) FROM device_report_metrics)
       );
"""
