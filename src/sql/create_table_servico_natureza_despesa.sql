CREATE TABLE servico_natureza_despesa (
cod_servico BIGINT NOT NULL,
cod_natureza_despesa varchar(50) NOT NULL,
nome_natureza_despesa varchar(200),
status_natureza_despesa BOOLEAN,
data_hora_carga TIMESTAMPTZ DEFAULT now(),
PRIMARY KEY (cod_servico, cod_natureza_despesa)
);
