CREATE TABLE material_caracteristica (
cod_item BIGINT NOT NULL REFERENCES material_item (cod_item),
numero_caracteristica BIGINT NOT NULL,
codigo_caracteristica varchar(100) NOT NULL,
codigo_valor_caracteristica varchar(100) NOT NULL,
nome_caracteristica varchar(200),
status_caracteristica BOOLEAN,
nome_valor_caracteristica varchar(200),
status_valor_caracteristica BOOLEAN,
item_sustentavel BOOLEAN,
status_item BOOLEAN,
sigla_unidade_medida varchar(50),
data_hora_atualizacao TIMESTAMP,
data_hora_carga TIMESTAMPTZ DEFAULT now(),
PRIMARY KEY (cod_item, numero_caracteristica, codigo_caracteristica, codigo_valor_caracteristica)
);
