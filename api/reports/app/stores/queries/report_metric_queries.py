import os

CREATE_REPORT_METRIC_QUERY = """
INSERT INTO report_metrics (name, abbreviation, unit, report_value_type)
     VALUES (:name, :abbreviation, :unit, :report_value_type)
  RETURNING report_metric_id, name, abbreviation, unit, report_value_type
"""

GET_REPORT_METRIC_QUERY_TEMPLATE = """
SELECT {fields}
  FROM report_metrics
 WHERE report_metric_id = :report_metric_id 
"""

GET_REPORT_METRIC_BY_NAME_QUERY_TEMPLATE = """
SELECT {fields}
  FROM report_metrics
 WHERE name = :name 
"""

GET_REPORT_METRIC_BY_ABBREVIATION_QUERY_TEMPLATE = """
SELECT {fields}
  FROM report_metrics
 WHERE abbreviation = :abbreviation 
"""

GET_REPORT_METRICS_QUERY_TEMPLATE = """
  SELECT {fields}
    FROM report_metrics
   WHERE {where_conditions}
ORDER BY {order_by_condition}
"""

UPDATE_REPORT_METRIC_QUERY = """
   UPDATE report_metrics
      SET {set_conditions}
    WHERE report_metric_id = :report_metric_id
RETURNING report_metric_id, name, abbreviation, unit, report_value_type
"""

DELETE_REPORT_METRIC_QUERY = """
DELETE FROM report_metrics
      WHERE report_metric_id = :report_metric_id
  RETURNING :report_metric_id
"""

BACKUP_REPORT_METRICS = f"""
     COPY report_metrics 
       TO '{os.environ.get("POSTGRES_BACKUP") or '/backup'}/report_metrics.csv' 
DELIMITER ',' 
      CSV 
   HEADER;
"""

LOAD_REPORT_METRICS_FROM_BACKUP = f"""
CREATE TABLE _report_metrics (LIKE report_metrics INCLUDING DEFAULTS);

     COPY _report_metrics
     FROM '{os.environ.get("POSTGRES_BACKUP") or '/backup'}/report_metrics.csv'
DELIMITER ',' 
      CSV 
   HEADER;

INSERT INTO report_metrics
     SELECT *
       FROM _report_metrics
ON CONFLICT
         DO NOTHING;

DROP TABLE _report_metrics;

SELECT setval(
       pg_get_serial_sequence('report_metrics','report_metric_id'), 
       (SELECT MAX(report_metric_id) FROM report_metrics)
       );
"""
