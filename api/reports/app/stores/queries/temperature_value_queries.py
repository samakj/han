import os

CREATE_TEMPERATURE_VALUE_QUERY = """
INSERT INTO temperature_values (temperature_value_id, value)
     VALUES (:temperature_value_id, :value)
  RETURNING temperature_value_id, report_id, value
"""

GET_TEMPERATURE_VALUE_QUERY_TEMPLATE = """
   SELECT {fields}
     FROM temperature_values
    WHERE temperature_value_id = :temperature_value_id
"""

GET_TEMPERATURE_VALUE_BY_REPORT_ID_QUERY_TEMPLATE = """
   SELECT {fields}
     FROM temperature_values
    WHERE temperature_value_id = :temperature_value_id
"""

GET_TEMPERATURE_VALUES_QUERY_TEMPLATE = """
   SELECT {fields}
     FROM temperature_values
 ORDER BY {order_by_condition}
    LIMIT {limit}
"""

UPDATE_TEMPERATURE_VALUE_QUERY = """
   UPDATE temperature_values
      SET {set_conditions}
    WHERE temperature_value_id = :temperature_value_id
RETURNING temperature_value_id, report_id, value
"""

DELETE_TEMPERATURE_VALUE_QUERY = """
DELETE FROM temperature_values
      WHERE temperature_value_id = :temperature_value_id
  RETURNING :temperature_value_id
"""

BACKUP_TEMPERATURE_VALUES = f"""
     COPY temperature_values 
       TO '{os.environ.get("POSTGRES_BACKUP") or '/backup'}/temperature_values.csv' 
DELIMITER ',' 
      CSV 
   HEADER;
"""

LOAD_TEMPERATURE_VALUES_FROM_BACKUP = f"""
CREATE TABLE _temperature_values (LIKE temperature_values INCLUDING DEFAULTS);

     COPY _temperature_values
     FROM '{os.environ.get("POSTGRES_BACKUP") or '/backup'}/temperature_values.csv'
DELIMITER ',' 
      CSV 
   HEADER;

INSERT INTO temperature_values
     SELECT *
       FROM _temperature_values
ON CONFLICT
         DO NOTHING;

DROP TABLE _temperature_values;

SELECT setval(
       pg_get_serial_sequence('temperature_values','temperature_value_id'), 
       (SELECT MAX(temperature_value_id) FROM temperature_values)
       );
"""
