import os

CREATE_DEVICE_TYPE_METRIC_QUERY = """
INSERT INTO device_type_metrics (device_type_id, metric_id)
     VALUES (:device_type_id, :metric_id)
  RETURNING device_type_metric_id, device_type_id, metric_id
"""

GET_DEVICE_TYPE_METRIC_QUERY_TEMPLATE = """
SELECT {fields}
  FROM device_type_metrics
 WHERE device_type_metric_id = :device_type_metric_id 
"""

GET_DEVICE_TYPE_METRICS_QUERY_TEMPLATE = """
  SELECT {fields}
    FROM device_type_metrics
   WHERE {where_conditions}
ORDER BY {order_by_condition}
"""

UPDATE_DEVICE_TYPE_METRIC_QUERY = """
   UPDATE device_type_metrics
      SET {set_conditions}
    WHERE device_type_metric_id = :device_type_metric_id
RETURNING device_type_metric_id, device_type_id, metric_id
"""

DELETE_DEVICE_TYPE_METRIC_QUERY = """
DELETE FROM device_type_metrics
      WHERE device_type_metric_id = :device_type_metric_id
  RETURNING :device_type_metric_id
"""

BACKUP_DEVICE_TYPE_METRICS = f"""
     COPY device_type_metrics 
       TO '{os.environ.get("POSTGRES_BACKUP") or '/backup'}/device_type_metrics.csv' 
DELIMITER ',' 
      CSV 
   HEADER;
"""

LOAD_DEVICE_TYPE_METRICS_FROM_BACKUP = f"""
CREATE TABLE _device_type_metrics (LIKE device_type_metrics INCLUDING DEFAULTS);

     COPY _device_type_metrics
     FROM '{os.environ.get("POSTGRES_BACKUP") or '/backup'}/device_type_metrics.csv'
DELIMITER ',' 
      CSV 
   HEADER;

INSERT INTO device_type_metrics
     SELECT *
       FROM _device_type_metrics
ON CONFLICT
         DO NOTHING;

DROP TABLE _device_type_metrics;

SELECT setval(
       pg_get_serial_sequence('device_type_metrics','device_type_metric_id'), 
       (SELECT MAX(device_type_metric_id) FROM device_type_metrics)
       );
"""
