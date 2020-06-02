CREATE TABLE IF NOT EXISTS reports
(
    report_id   BIGSERIAL PRIMARY KEY,
    reported_at TIMESTAMP NOT NULL DEFAULT (now() AT TIME ZONE 'utc'),
    device_id   TEXT      NOT NULL REFERENCES devices (device_id),
    metric_id   INT       NOT NULL REFERENCES metrics (metric_id),
    value       TEXT      NOT NULL
);
