import os

CREATE_HUMIDITY_VALUE_QUERY = """
INSERT INTO humidity_values (humidity_value_id, value)
     VALUES (:humidity_value_id, :value)
  RETURNING humidity_value_id, report_id, value
"""

GET_HUMIDITY_VALUE_QUERY_TEMPLATE = """
   SELECT {fields}
     FROM humidity_values
    WHERE humidity_value_id = :humidity_value_id
"""

GET_HUMIDITY_VALUE_BY_REPORT_ID_QUERY_TEMPLATE = """
   SELECT {fields}
     FROM humidity_values
    WHERE humidity_value_id = :humidity_value_id
"""

GET_HUMIDITY_VALUES_QUERY_TEMPLATE = """
   SELECT {fields}
     FROM humidity_values
 ORDER BY {order_by_condition}
    LIMIT {limit}
"""

UPDATE_HUMIDITY_VALUE_QUERY = """
   UPDATE humidity_values
      SET {set_conditions}
    WHERE humidity_value_id = :humidity_value_id
RETURNING humidity_value_id, report_id, value
"""

DELETE_HUMIDITY_VALUE_QUERY = """
DELETE FROM humidity_values
      WHERE humidity_value_id = :humidity_value_id
  RETURNING :humidity_value_id
"""

BACKUP_HUMIDITY_VALUES = f"""
     COPY humidity_values 
       TO '{os.environ.get("POSTGRES_BACKUP") or '/backup'}/humidity_values.csv' 
DELIMITER ',' 
      CSV 
   HEADER;
"""

LOAD_HUMIDITY_VALUES_FROM_BACKUP = f"""
CREATE TABLE _humidity_values (LIKE humidity_values INCLUDING DEFAULTS);

     COPY _humidity_values
     FROM '{os.environ.get("POSTGRES_BACKUP") or '/backup'}/humidity_values.csv'
DELIMITER ',' 
      CSV 
   HEADER;

INSERT INTO humidity_values
     SELECT *
       FROM _humidity_values
ON CONFLICT
         DO NOTHING;

DROP TABLE _humidity_values;

SELECT setval(
       pg_get_serial_sequence('humidity_values','humidity_value_id'), 
       (SELECT MAX(humidity_value_id) FROM humidity_values)
       );
"""
