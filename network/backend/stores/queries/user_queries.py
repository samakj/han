import os

CREATE_USER_QUERY = """
INSERT INTO users (username, password, mac_address)
     VALUES (:username, :password, :mac_address)
  RETURNING user_id, username, mac_address
"""

GET_USER_QUERY_TEMPLATE = """
SELECT {fields}
  FROM users
 WHERE user_id = :user_id 
"""

GET_USER_BY_USERNAME_QUERY_TEMPLATE = """
SELECT {fields}
  FROM users
 WHERE username = :username 
"""

GET_USER_BY_MAC_ADDRESS_QUERY_TEMPLATE = """
SELECT {fields}
  FROM users
 WHERE mac_address = :mac_address 
"""

GET_USERS_QUERY_TEMPLATE = """
  SELECT {fields}
    FROM users
   WHERE {where_conditions}
ORDER BY {order_by_condition}
"""

UPDATE_USER_QUERY_TEMPLATE = """
   UPDATE users
      SET {set_conditions}
    WHERE user_id = :user_id
RETURNING user_id, username, mac_address
"""

DELETE_USER_QUERY = """
DELETE FROM users
      WHERE user_id = :user_id
  RETURNING :user_id
"""

BACKUP_USERS = f"""
     COPY users 
       TO '{os.environ.get("POSTGRES_BACKUP") or '/backup'}/users.csv' 
DELIMITER ',' 
      CSV 
   HEADER;
"""

LOAD_USERS_FROM_BACKUP = f"""
CREATE TABLE _users (LIKE users INCLUDING DEFAULTS);

     COPY _users
     FROM '{os.environ.get("POSTGRES_BACKUP") or '/backup'}/users.csv'
DELIMITER ',' 
      CSV 
   HEADER;

INSERT INTO users
     SELECT *
       FROM _users
ON CONFLICT
         DO NOTHING;

DROP TABLE _users;

SELECT setval(
       pg_get_serial_sequence('users','user_id'), 
       (SELECT MAX(user_id) FROM users)
       );
"""
