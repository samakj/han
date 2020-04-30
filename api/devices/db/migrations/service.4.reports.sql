CREATE TABLE IF NOT EXISTS float_report_values
(
    float_report_value_id SERIAL PRIMARY KEY,
    value                 DECIMAL(16, 8) NOT NULL
);

CREATE TABLE IF NOT EXISTS string_report_values
(
    string_report_value_id SERIAL PRIMARY KEY,
    value                  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bool_report_values
(
    bool_report_value_id SERIAL PRIMARY KEY,
    value                BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS reports
(
    report_id        SERIAL PRIMARY KEY,
    device_id        TEXT      NOT NULL REFERENCES devices (device_id),
    report_metric_id INTEGER   NOT NULL REFERENCES report_metrics (report_metric_id),
    reported_at      TIMESTAMP NOT NULL DEFAULT (now() AT TIME ZONE 'utc'),
    value_id         INTEGER   NOT NUll
);
