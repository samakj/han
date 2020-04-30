CREATE_REPORT_METRIC_QUERY = """
INSERT INTO report_metrics (report_metric_id, name, abbreviation, unit, report_value_type)
     VALUES (:report_metric_id, :name, :abbreviation, :unit, :report_value_type)
  RETURNING report_metric_id, name, abbreviation, unit, report_value_type
"""

GET_REPORT_METRIC_QUERY_TEMPLATE = """
SELECT {fields}
  FROM report_metrics
 WHERE report_metric_id = :report_metric_id 
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
