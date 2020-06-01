import os

CREATE_SUPERUSER_QUERY = """
INSERT INTO superusers (user_id)
     VALUES (:user_id)
  RETURNING superuser_id, user_id
"""

GET_SUPERUSER_QUERY_TEMPLATE = """
SELECT {fields}
  FROM superusers
 WHERE superuser_id = :superuser_id 
"""

GET_SUPERUSER_BY_USER_ID_QUERY_TEMPLATE = """
SELECT {fields}
  FROM superusers
 WHERE user_id = :user_id 
"""

GET_SUPERUSERS_QUERY_TEMPLATE = """
  SELECT {fields}
    FROM superusers
   WHERE {where_conditions}
ORDER BY {order_by_condition}
"""

UPDATE_SUPERUSER_QUERY_TEMPLATE = """
   UPDATE superusers
      SET {set_conditions}
    WHERE superuser_id = :superuser_id
RETURNING superuser_id, user_id
"""

DELETE_SUPERUSER_QUERY = """
DELETE FROM superusers
      WHERE superuser_id = :superuser_id
  RETURNING :superuser_id
"""

BACKUP_SUPERUSERS = f"""
     COPY superusers 
       TO '{os.environ.get("POSTGRES_BACKUP") or '/backup'}/superusers.csv' 
DELIMITER ',' 
      CSV 
   HEADER;
"""

LOAD_SUPERUSERS_FROM_BACKUP = f"""
CREATE TABLE _superusers (LIKE superusers INCLUDING DEFAULTS);

     COPY _superusers
     FROM '{os.environ.get("POSTGRES_BACKUP") or '/backup'}/superusers.csv'
DELIMITER ',' 
      CSV 
   HEADER;

INSERT INTO superusers
     SELECT *
       FROM _superusers
ON CONFLICT
         DO NOTHING;

DROP TABLE _superusers;

SELECT setval(
       pg_get_serial_sequence('superusers','superuser_id'), 
       (SELECT MAX(superuser_id) FROM superusers)
       );
"""
