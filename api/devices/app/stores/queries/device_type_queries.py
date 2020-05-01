import os

CREATE_DEVICE_TYPE_QUERY = """
INSERT INTO device_types (name)
     VALUES (:name)
  RETURNING device_type_id, name
"""

GET_DEVICE_TYPE_QUERY_TEMPLATE = """
SELECT {fields}
  FROM device_types
 WHERE device_type_id = :device_type_id 
"""

GET_DEVICE_TYPE_BY_NAME_QUERY_TEMPLATE = """
SELECT {fields}
  FROM device_types
 WHERE name = :name 
"""

GET_DEVICE_TYPES_QUERY_TEMPLATE = """
  SELECT {fields}
    FROM device_types
   WHERE {where_conditions}
ORDER BY {order_by_condition}
"""

UPDATE_DEVICE_TYPE_QUERY = """
   UPDATE device_types
      SET {set_conditions}
    WHERE device_type_id = :device_type_id
RETURNING device_type_id, name 
"""

DELETE_DEVICE_TYPE_QUERY = """
DELETE FROM device_types
      WHERE device_type_id = :device_type_id
  RETURNING :device_type_id
"""

BACKUP_DEVICE_TYPES = f"""
     COPY device_types 
       TO '{os.environ.get("POSTGRES_BACKUP") or '/backup'}/device_types.csv' 
DELIMITER ',' 
      CSV 
   HEADER;
"""

LOAD_DEVICE_TYPES_FROM_BACKUP = f"""
CREATE TABLE _device_types (LIKE device_types INCLUDING DEFAULTS);

     COPY _device_types
     FROM '{os.environ.get("POSTGRES_BACKUP") or '/backup'}/device_types.csv'
DELIMITER ',' 
      CSV 
   HEADER;

INSERT INTO device_types
     SELECT *
       FROM _device_types
ON CONFLICT
         DO NOTHING;

DROP TABLE _device_types;
"""
