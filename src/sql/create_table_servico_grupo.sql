CREATE TABLE servico_grupo (
cod_grupo BIGINT PRIMARY KEY,
cod_divisao BIGINT NOT NULL REFERENCES servico_divisao (cod_divisao),
nome_secao varchar(200),
nome_divisao varchar(200) NOT NULL,
nome_grupo varchar(200) NOT NULL,
status_grupo BOOLEAN,
data_hora_atualizacao TIMESTAMP,
data_hora_carga TIMESTAMPTZ DEFAULT now()
);
