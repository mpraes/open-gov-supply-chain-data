CREATE TABLE servico_unidade_medida (
cod_servico BIGINT NOT NULL,
sigla_unidade_medida varchar(50) NOT NULL,
nome_unidade_medida varchar(200),
status_unidade_medida BOOLEAN,
data_hora_carga TIMESTAMPTZ DEFAULT now(),
PRIMARY KEY (cod_servico, sigla_unidade_medida)
);
