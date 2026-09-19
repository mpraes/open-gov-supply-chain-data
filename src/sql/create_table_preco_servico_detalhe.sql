CREATE TABLE preco_servico_detalhe (
id_compra TEXT NOT NULL,
id_item_compra BIGINT NOT NULL,
numero_item_compra BIGINT,
codigo_item_catalogo BIGINT NOT NULL,
objeto_compra TEXT,
descricao_detalhada_item TEXT,
data_atualizacao_fato TIMESTAMP,
data_hora_carga TIMESTAMPTZ DEFAULT now(),
PRIMARY KEY (id_compra, id_item_compra)
);
