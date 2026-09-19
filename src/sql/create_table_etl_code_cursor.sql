CREATE TABLE IF NOT EXISTS etl_code_cursor (
job_name TEXT PRIMARY KEY,
last_code BIGINT NOT NULL,
updated_at TIMESTAMPTZ DEFAULT now()
);
