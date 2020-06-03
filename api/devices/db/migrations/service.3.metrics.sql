CREATE TABLE IF NOT EXISTS metrics
(
    metric_id    SERIAL PRIMARY KEY,
    name         TEXT UNIQUE NOT NULL,
    abbreviation TEXT UNIQUE NOT NULL,
    value_type   TEXT        NOT NULL,
    unit         TEXT
);

CREATE TABLE IF NOT EXISTS device_type_metrics
(
    device_type_metric_id SERIAL PRIMARY KEY,
    device_type_id        INTEGER NOT NULL REFERENCES device_types (device_type_id),
    metric_id             INTEGER NOT NULL REFERENCES metrics (metric_id),
    reportable            BOOLEAN NOT NULL,
    commandable           BOOLEAN NOT NULL
);
