CREATE TABLE pgc_agregacao (
orgao varchar(32) NOT NULL,
ano BIGINT NOT NULL,
poder varchar(50),
esfera varchar(50),
data_hora_publicacao_pncp TIMESTAMP,
data_hora_atualizacao TIMESTAMP,
quantidade_total_itens BIGINT,
valor_total_estimado NUMERIC,
data_hora_carga TIMESTAMPTZ DEFAULT now(),
PRIMARY KEY (orgao, ano)
);
