CREATE TABLE IF NOT EXISTS device_types
(
    device_type_id SERIAL PRIMARY KEY,
    name           TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS devices
(
    device_id      TEXT PRIMARY KEY,
    device_type_id INTEGER NOT NULL REFERENCES device_types (device_type_id)
);
