CREATE TABLE fornecedor (
ni_fornecedor TEXT NOT NULL,
ativo TEXT,
cnpj TEXT,
cpf TEXT,
habilitado_licitar TEXT,
codigo_cnae TEXT,
nome_cnae TEXT,
nome_municipio TEXT,
natureza_juridica_id TEXT,
natureza_juridica_nome TEXT,
porte_empresa_id TEXT,
porte_empresa_nome TEXT,
nome_razao_social_fornecedor TEXT,
uf_sigla TEXT,
data_hora_carga TIMESTAMPTZ DEFAULT now(),
PRIMARY KEY (ni_fornecedor)
);
