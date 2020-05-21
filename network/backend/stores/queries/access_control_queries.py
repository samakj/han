import os

CREATE_ACCESS_CONTROL_QUERY = """
INSERT INTO access_controls (user_id, topic, action)
     VALUES (:user_id, :topic, :action)
  RETURNING access_control_id, user_id, topic, action
"""

GET_ACCESS_CONTROL_QUERY_TEMPLATE = """
SELECT {fields}
  FROM access_controls
 WHERE access_control_id = :access_control_id 
"""

GET_ACCESS_CONTROLS_QUERY_TEMPLATE = """
  SELECT {fields}
    FROM access_controls
   WHERE {where_conditions}
ORDER BY {order_by_condition}
"""

UPDATE_ACCESS_CONTROL_QUERY_TEMPLATE = """
   UPDATE access_controls
      SET {set_conditions}
    WHERE access_control_id = :access_control_id
RETURNING access_control_id, user_id, topic, action
"""

DELETE_ACCESS_CONTROL_QUERY = """
DELETE FROM access_controls
      WHERE access_control_id = :access_control_id
  RETURNING :access_control_id
"""

BACKUP_ACCESS_CONTROLS = f"""
     COPY access_controls 
       TO '{os.environ.get("POSTGRES_BACKUP") or '/backup'}/access_controls.csv' 
DELIMITER ',' 
      CSV 
   HEADER;
"""

LOAD_ACCESS_CONTROLS_FROM_BACKUP = f"""
CREATE TABLE _access_controls (LIKE access_controls INCLUDING DEFAULTS);

     COPY _access_controls
     FROM '{os.environ.get("POSTGRES_BACKUP") or '/backup'}/access_controls.csv'
DELIMITER ',' 
      CSV 
   HEADER;

INSERT INTO access_controls
     SELECT *
       FROM _access_controls
ON CONFLICT
         DO NOTHING;

DROP TABLE _access_controls;

SELECT setval(
       pg_get_serial_sequence('access_controls','access_control_id'), 
       (SELECT MAX(access_control_id) FROM access_controls)
       );
"""
