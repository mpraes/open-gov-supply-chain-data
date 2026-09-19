CREATE TABLE servico_secao (
cod_secao BIGINT PRIMARY KEY,
nome_secao varchar(200) NOT NULL,
status_secao BOOLEAN,
data_hora_atualizacao TIMESTAMP,
data_hora_carga TIMESTAMPTZ DEFAULT now()
);
