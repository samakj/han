import os

CREATE_DEVICE_QUERY = """
INSERT INTO devices (device_id, device_type_id, latest_ping)
     VALUES (:device_id, :device_type_id, :latest_ping)
  RETURNING device_id, device_type_id, latest_ping
"""

GET_DEVICE_QUERY_TEMPLATE = """
SELECT {fields}
  FROM devices
 WHERE device_id = :device_id 
"""

GET_DEVICES_QUERY_TEMPLATE = """
  SELECT {fields}
    FROM devices
   WHERE {where_conditions}
ORDER BY {order_by_condition}
"""

UPDATE_DEVICE_QUERY = """
   UPDATE devices
      SET {set_conditions}
    WHERE device_id = :device_id
RETURNING device_id, device_type_id, latest_ping
"""

DELETE_DEVICE_QUERY = """
DELETE FROM devices
      WHERE device_id = :device_id
  RETURNING :device_id
"""

BACKUP_DEVICES = f"""
     COPY devices 
       TO '{os.environ.get("POSTGRES_BACKUP") or '/backup'}/devices.csv' 
DELIMITER ',' 
      CSV 
   HEADER;
"""

LOAD_DEVICES_FROM_BACKUP = f"""
CREATE TABLE _devices (LIKE devices INCLUDING DEFAULTS);

     COPY _devices
     FROM '{os.environ.get("POSTGRES_BACKUP") or '/backup'}/devices.csv'
DELIMITER ',' 
      CSV 
   HEADER;

INSERT INTO devices
     SELECT *
       FROM _devices
ON CONFLICT
         DO NOTHING;

DROP TABLE _devices;
"""
