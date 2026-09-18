CREATE TABLE material_class (
cod_classe BIGINT PRIMARY KEY,
cod_grupo BIGINT NOT NULL REFERENCES material_group (cod_grupo),
nome_grupo varchar(200) NOT NULL,
nome_classe varchar(200) NOT NULL,
status_classe BOOLEAN,
data_hora_atualizacao TIMESTAMP,
data_hora_carga TIMESTAMPTZ DEFAULT now()
);
