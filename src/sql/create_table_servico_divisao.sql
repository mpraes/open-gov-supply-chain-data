CREATE TABLE servico_divisao (
cod_divisao BIGINT PRIMARY KEY,
cod_secao BIGINT NOT NULL REFERENCES servico_secao (cod_secao),
nome_secao varchar(200) NOT NULL,
nome_divisao varchar(200) NOT NULL,
status_divisao BOOLEAN,
data_hora_atualizacao TIMESTAMP,
data_hora_carga TIMESTAMPTZ DEFAULT now()
);
