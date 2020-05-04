import os

CREATE_MOTION_VALUE_QUERY = """
INSERT INTO motion_values (motion_value_id, value)
     VALUES (:motion_value_id, :value)
  RETURNING motion_value_id, report_id, value
"""

GET_MOTION_VALUE_QUERY_TEMPLATE = """
   SELECT {fields}
     FROM motion_values
    WHERE motion_value_id = :motion_value_id
"""

GET_MOTION_VALUE_BY_REPORT_ID_QUERY_TEMPLATE = """
   SELECT {fields}
     FROM motion_values
    WHERE motion_value_id = :motion_value_id
"""

GET_MOTION_VALUES_QUERY_TEMPLATE = """
   SELECT {fields}
     FROM motion_values
 ORDER BY {order_by_condition}
    LIMIT {limit}
"""

UPDATE_MOTION_VALUE_QUERY = """
   UPDATE motion_values
      SET {set_conditions}
    WHERE motion_value_id = :motion_value_id
RETURNING motion_value_id, report_id, value
"""

DELETE_MOTION_VALUE_QUERY = """
DELETE FROM motion_values
      WHERE motion_value_id = :motion_value_id
  RETURNING :motion_value_id
"""

BACKUP_MOTION_VALUES = f"""
     COPY motion_values 
       TO '{os.environ.get("POSTGRES_BACKUP") or '/backup'}/motion_values.csv' 
DELIMITER ',' 
      CSV 
   HEADER;
"""

LOAD_MOTION_VALUES_FROM_BACKUP = f"""
CREATE TABLE _motion_values (LIKE motion_values INCLUDING DEFAULTS);

     COPY _motion_values
     FROM '{os.environ.get("POSTGRES_BACKUP") or '/backup'}/motion_values.csv'
DELIMITER ',' 
      CSV 
   HEADER;

INSERT INTO motion_values
     SELECT *
       FROM _motion_values
ON CONFLICT
         DO NOTHING;

DROP TABLE _motion_values;

SELECT setval(
       pg_get_serial_sequence('motion_values','motion_value_id'), 
       (SELECT MAX(motion_value_id) FROM motion_values)
       );
"""
