CREATE TABLE alice_aviso (
ticket_analise TEXT NOT NULL,
chave_compra TEXT,
msg_erro TEXT,
data_solicitacao_analise TEXT,
data_encerramento_analise TEXT,
tipo_analise TEXT,
codigo_status_analise TEXT,
descricao_status_analise TEXT,
data_hora_carga TIMESTAMPTZ DEFAULT now(),
PRIMARY KEY (ticket_analise)
);
