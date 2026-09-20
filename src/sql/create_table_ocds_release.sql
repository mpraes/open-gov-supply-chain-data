CREATE TABLE ocds_release (
ocid TEXT NOT NULL,
id TEXT NOT NULL,
date TEXT,
initiation_type TEXT,
language TEXT,
buyer_id TEXT,
buyer_name TEXT,
tender_id TEXT,
tender_title TEXT,
release_json TEXT,
data_hora_carga TIMESTAMPTZ DEFAULT now(),
PRIMARY KEY (ocid, id)
);
