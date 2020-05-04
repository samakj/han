CREATE TABLE IF NOT EXISTS report_metrics
(
    report_metric_id  SERIAL PRIMARY KEY,
    name              TEXT UNIQUE NOT NULL,
    abbreviation      TEXT UNIQUE NOT NULL,
    unit              TEXT,
    report_value_type TEXT
);
