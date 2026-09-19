CREATE TABLE servico_classe (
cod_classe BIGINT PRIMARY KEY,
cod_grupo BIGINT NOT NULL REFERENCES servico_grupo (cod_grupo),
nome_grupo varchar(200) NOT NULL,
nome_classe varchar(200) NOT NULL,
status_classe BOOLEAN,
data_hora_atualizacao TIMESTAMP,
data_hora_carga TIMESTAMPTZ DEFAULT now()
);
