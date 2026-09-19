CREATE TABLE servico_item (
cod_servico BIGINT PRIMARY KEY,
cod_secao BIGINT,
nome_secao varchar(200),
cod_divisao BIGINT,
nome_divisao varchar(200),
cod_grupo BIGINT,
nome_grupo varchar(200),
cod_classe BIGINT,
nome_classe varchar(200),
cod_subclasse BIGINT,
nome_subclasse varchar(200),
nome_servico varchar(500) NOT NULL,
cod_cpc BIGINT,
exclusivo_central_compras BOOLEAN,
status_servico BOOLEAN,
data_hora_atualizacao TIMESTAMP,
data_hora_carga TIMESTAMPTZ DEFAULT now()
);
