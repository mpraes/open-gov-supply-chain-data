CREATE TABLE servico_subclasse (
cod_subclasse BIGINT PRIMARY KEY,
cod_classe BIGINT NOT NULL,
nome_classe varchar(200) NOT NULL,
nome_subclasse varchar(200) NOT NULL,
status_subclasse BOOLEAN,
data_hora_atualizacao TIMESTAMP,
data_hora_carga TIMESTAMPTZ DEFAULT now()
);
