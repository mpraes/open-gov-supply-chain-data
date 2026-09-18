CREATE TABLE material_pdm (
cod_pdm BIGINT PRIMARY KEY,
cod_classe BIGINT NOT NULL REFERENCES material_class (cod_classe),
cod_grupo BIGINT NOT NULL,
nome_grupo varchar(200) NOT NULL,
nome_classe varchar(200) NOT NULL,
nome_pdm varchar(200) NOT NULL,
status_pdm BOOLEAN,
data_hora_atualizacao TIMESTAMP,
data_hora_carga TIMESTAMPTZ DEFAULT now()
);
