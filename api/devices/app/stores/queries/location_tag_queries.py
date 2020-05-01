import os

CREATE_LOCATION_TAG_QUERY = """
INSERT INTO location_tags (name, level)
     VALUES (:name, :level)
  RETURNING location_tag_id, name, level
"""

GET_LOCATION_TAG_QUERY_TEMPLATE = """
SELECT {fields}
  FROM location_tags
 WHERE location_tag_id = :location_tag_id 
"""

GET_LOCATION_TAG_BY_NAME_QUERY_TEMPLATE = """
SELECT {fields}
  FROM location_tags
 WHERE name = :name 
"""

GET_LOCATION_TAGS_QUERY_TEMPLATE = """
  SELECT {fields}
    FROM location_tags
   WHERE {where_conditions}
ORDER BY {order_by_condition}
"""

UPDATE_LOCATION_TAG_QUERY = """
   UPDATE location_tags
      SET {set_conditions}
    WHERE location_tag_id = :location_tag_id
RETURNING location_tag_id, name, level
"""

DELETE_LOCATION_TAG_QUERY = """
DELETE FROM location_tags
      WHERE location_tag_id = :location_tag_id
  RETURNING :location_tag_id
"""

BACKUP_LOCATION_TAGS = f"""
     COPY location_tags 
       TO '{os.environ.get("POSTGRES_BACKUP") or '/backup'}/location_tags.csv' 
DELIMITER ',' 
      CSV 
   HEADER;
"""

LOAD_LOCATION_TAGS_FROM_BACKUP = f"""
CREATE TABLE _location_tags (LIKE location_tags INCLUDING DEFAULTS);

     COPY _location_tags
     FROM '{os.environ.get("POSTGRES_BACKUP") or '/backup'}/location_tags.csv'
DELIMITER ',' 
      CSV 
   HEADER;

INSERT INTO location_tags
     SELECT *
       FROM _location_tags
ON CONFLICT
         DO NOTHING;

DROP TABLE _location_tags;

SELECT setval(
       pg_get_serial_sequence('location_tags','location_tag_id'), 
       (SELECT MAX(location_tag_id) FROM location_tags)
       );
"""
