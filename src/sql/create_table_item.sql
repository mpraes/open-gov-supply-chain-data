CREATE TABLE material_item (
cod_item BIGINT PRIMARY KEY,
cod_grupo BIGINT NOT NULL,
nome_grupo varchar(200) NOT NULL,
cod_classe BIGINT NOT NULL,
nome_classe varchar(200) NOT NULL,
cod_pdm BIGINT NOT NULL REFERENCES material_pdm (cod_pdm),
nome_pdm varchar(200) NOT NULL,
descricao_item TEXT NOT NULL,
status_item BOOLEAN,
item_sustentavel BOOLEAN,
codigo_ncm varchar(20),
descricao_ncm TEXT,
aplica_margem_preferencia BOOLEAN,
data_hora_atualizacao TIMESTAMP,
data_hora_carga TIMESTAMPTZ DEFAULT now()
);
