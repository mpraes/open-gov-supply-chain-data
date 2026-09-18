CREATE TABLE material_unidade_fornecimento (
cod_pdm BIGINT NOT NULL REFERENCES material_pdm (cod_pdm),
numero_sequencial_unidade_fornecimento BIGINT NOT NULL,
sigla_unidade_fornecimento varchar(50) NOT NULL,
nome_unidade_fornecimento varchar(200),
descricao_unidade_fornecimento TEXT,
sigla_unidade_medida varchar(50),
capacidade_unidade_fornecimento NUMERIC,
status_unidade_fornecimento_pdm BOOLEAN,
status_unidade_fornecimento BOOLEAN,
data_hora_atualizacao TIMESTAMP,
data_hora_carga TIMESTAMPTZ DEFAULT now(),
PRIMARY KEY (cod_pdm, numero_sequencial_unidade_fornecimento)
);
