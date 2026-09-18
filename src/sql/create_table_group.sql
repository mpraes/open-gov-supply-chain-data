CREATE TABLE material_group (
cod_grupo BIGINT PRIMARY KEY,
nome_grupo varchar(200) NOT NULL,
status_grupo BOOLEAN,
data_hora_atualizacao TIMESTAMP,
data_hora_carga TIMESTAMPTZ DEFAULT now()
);
