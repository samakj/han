import os

CREATE_REPORT_QUERY = """
INSERT INTO reports (reported_at, device_id, metric_id, value)
     VALUES (:reported_at, :device_id, :metric_id, :value)
  RETURNING report_id, reported_at, device_id, metric_id, value
"""

GET_REPORT_QUERY_TEMPLATE = """
SELECT {fields}
  FROM reports
 WHERE report_id = :report_id
"""

GET_REPORTS_QUERY_TEMPLATE = """
  SELECT {fields}
    FROM reports
   WHERE {where_conditions}
ORDER BY {order_by_condition}
   LIMIT {limit}
"""

UPDATE_REPORT_QUERY = """
   UPDATE reports
      SET {set_conditions}
    WHERE report_id = :report_id
RETURNING report_id, reported_at, device_id, metric_id, value
"""

DELETE_REPORT_QUERY = """
DELETE FROM reports
      WHERE report_id = :report_id
  RETURNING :report_id
"""

BACKUP_REPORTS = f"""
     COPY reports 
       TO '{os.environ.get("POSTGRES_BACKUP") or '/backup'}/reports.csv' 
DELIMITER ',' 
      CSV 
   HEADER;
"""

LOAD_REPORTS_FROM_BACKUP = f"""
CREATE TABLE _reports (LIKE reports INCLUDING DEFAULTS);

     COPY _reports
     FROM '{os.environ.get("POSTGRES_BACKUP") or '/backup'}/reports.csv'
DELIMITER ',' 
      CSV 
   HEADER;

INSERT INTO reports
     SELECT *
       FROM _reports
ON CONFLICT
         DO NOTHING;

DROP TABLE _reports;

SELECT setval(
       pg_get_serial_sequence('reports','report_id'), 
       (SELECT MAX(report_id) FROM reports)
       );
"""
