CREATE_DEVICE_LOCATION_TAG_QUERY = """
INSERT INTO device_location_tags (device_location_tag_id, device_id, location_tag_id)
     VALUES (:device_location_tag_id, :device_id, :location_tag_id)
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
