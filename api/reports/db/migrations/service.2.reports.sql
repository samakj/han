CREATE TABLE IF NOT EXISTS reports
(
    report_id        BIGSERIAL PRIMARY KEY,
    report_metric_id INT       NOT NULL REFERENCES report_metrics (report_metric_id),
    reported_at      TIMESTAMP NOT NULL DEFAULT (now() AT TIME ZONE 'utc'),
    device_id        TEXT      NOT NULL
);

CREATE TABLE IF NOT EXISTS temperature_values
(
    temperature_value_id BIGSERIAL PRIMARY KEY,
    report_id            BIGINT UNIQUE NOT NULL REFERENCES reports (report_id),
    value                DECIMAL(8, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS humidity_values
(
    humidity_value_id BIGSERIAL PRIMARY KEY,
    report_id         BIGINT UNIQUE NOT NULL REFERENCES reports (report_id),
    value             DECIMAL(8, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS motion_values
(
    humidity_value_id BIGSERIAL PRIMARY KEY,
    report_id         BIGINT UNIQUE NOT NULL REFERENCES reports (report_id),
    value             BOOLEAN       NOT NULL
);
