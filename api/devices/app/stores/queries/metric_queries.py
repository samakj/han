import os

CREATE_METRIC_QUERY = """
INSERT INTO metrics (name, abbreviation, value_type, unit)
     VALUES (:name, :abbreviation, :value_type, :unit)
  RETURNING metric_id, name, abbreviation, value_type, unit
"""

GET_METRIC_QUERY_TEMPLATE = """
SELECT {fields}
  FROM metrics
 WHERE metric_id = :metric_id 
"""

GET_METRIC_BY_NAME_QUERY_TEMPLATE = """
SELECT {fields}
  FROM metrics
 WHERE name = :name 
"""

GET_METRIC_BY_ABBREVIATION_QUERY_TEMPLATE = """
SELECT {fields}
  FROM metrics
 WHERE abbreviation = :abbreviation 
"""

GET_METRICS_QUERY_TEMPLATE = """
  SELECT {fields}
    FROM metrics
   WHERE {where_conditions}
ORDER BY {order_by_condition}
"""

UPDATE_METRIC_QUERY = """
   UPDATE metrics
      SET {set_conditions}
    WHERE metric_id = :metric_id
RETURNING metric_id, name, abbreviation, value_type, unit
"""

DELETE_METRIC_QUERY = """
DELETE FROM metrics
      WHERE metric_id = :metric_id
  RETURNING :metric_id
"""

BACKUP_METRICS = f"""
     COPY metrics 
       TO '{os.environ.get("POSTGRES_BACKUP") or '/backup'}/metrics.csv' 
DELIMITER ',' 
      CSV 
   HEADER;
"""

LOAD_METRICS_FROM_BACKUP = f"""
CREATE TABLE _metrics (LIKE metrics INCLUDING DEFAULTS);

     COPY _metrics
     FROM '{os.environ.get("POSTGRES_BACKUP") or '/backup'}/metrics.csv'
DELIMITER ',' 
      CSV 
   HEADER;

INSERT INTO metrics
     SELECT *
       FROM _metrics
ON CONFLICT
         DO NOTHING;

DROP TABLE _metrics;

SELECT setval(
       pg_get_serial_sequence('metrics','metric_id'), 
       (SELECT MAX(metric_id) FROM metrics)
       );
"""
