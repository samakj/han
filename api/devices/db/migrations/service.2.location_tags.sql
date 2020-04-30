CREATE TABLE IF NOT EXISTS location_tags
(
    location_tag_id SERIAL PRIMARY KEY,
    name            TEXT UNIQUE NOT NULL,
    level        INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS device_location_tags
(
    device_location_tag_id SERIAL PRIMARY KEY,
    device_id              TEXT    NOT NULL REFERENCES devices (device_id),
    location_tag_id        INTEGER NOT NULL REFERENCES location_tags (location_tag_id)
);
