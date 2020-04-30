CREATE_LOCATION_TAG_QUERY = """
INSERT INTO location_tags (location_tag_id, name, level)
     VALUES (:location_tag_id, :name, :level)
  RETURNING location_tag_id, name
"""

GET_LOCATION_TAG_QUERY_TEMPLATE = """
SELECT {fields}
  FROM location_tags
 WHERE location_tag_id = :location_tag_id 
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
