CREATE TABLE IF NOT EXISTS report_metrics
(
    report_metric_id  SERIAL PRIMARY KEY,
    name              TEXT UNIQUE NOT NULL,
    abbreviation      TEXT UNIQUE NOT NULL,
    unit              TEXT,
    report_value_type TEXT
);

CREATE TABLE IF NOT EXISTS device_type_report_metrics
(
    device_type_report_metric_id SERIAL PRIMARY KEY,
    device_type_id               INTEGER NOT NULL REFERENCES device_types (device_type_id),
    report_metric_id             INTEGER NOT NULL REFERENCES report_metrics (report_metric_id)
);
