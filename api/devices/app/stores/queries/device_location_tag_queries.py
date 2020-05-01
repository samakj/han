import os

CREATE_DEVICE_LOCATION_TAG_QUERY = """
INSERT INTO device_location_tags (device_id, location_tag_id)
     VALUES (:device_id, :location_tag_id)
  RETURNING device_location_tag_id, device_id, location_tag_id
"""

GET_DEVICE_LOCATION_TAG_QUERY_TEMPLATE = """
SELECT {fields}
  FROM device_location_tags
 WHERE device_location_tag_id = :device_location_tag_id 
"""

GET_DEVICE_LOCATION_TAGS_QUERY_TEMPLATE = """
  SELECT {fields}
    FROM device_location_tags
   WHERE {where_conditions}
ORDER BY {order_by_condition}
"""

UPDATE_DEVICE_LOCATION_TAG_QUERY = """
   UPDATE device_location_tags
      SET {set_conditions}
    WHERE device_location_tag_id = :device_location_tag_id
RETURNING device_location_tag_id, device_id, location_tag_id
"""

DELETE_DEVICE_LOCATION_TAG_QUERY = """
DELETE FROM device_location_tags
      WHERE device_location_tag_id = :device_location_tag_id
  RETURNING :device_location_tag_id
"""

BACKUP_DEVICE_LOCATION_TAGS = f"""
     COPY device_location_tags 
       TO '{os.environ.get("POSTGRES_BACKUP") or '/backup'}/device_location_tags.csv' 
DELIMITER ',' 
      CSV 
   HEADER;
"""

LOAD_DEVICE_LOCATION_TAGS_FROM_BACKUP = f"""
CREATE TABLE _device_location_tags (LIKE device_location_tags INCLUDING DEFAULTS);

     COPY _device_location_tags
     FROM '{os.environ.get("POSTGRES_BACKUP") or '/backup'}/device_location_tags.csv'
DELIMITER ',' 
      CSV 
   HEADER;

INSERT INTO device_location_tags
     SELECT *
       FROM _device_location_tags
ON CONFLICT
         DO NOTHING;

DROP TABLE _device_location_tags;

SELECT setval(
       pg_get_serial_sequence('device_location_tags','device_location_tag_id'), 
       (SELECT MAX(device_location_tag_id) FROM device_location_tags)
       );
"""
