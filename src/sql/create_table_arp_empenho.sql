CREATE TABLE arp_empenho (
numero_ata TEXT NOT NULL,
unidade_gerenciadora TEXT NOT NULL,
numero_item TEXT NOT NULL,
unidade TEXT NOT NULL,
tipo TEXT,
quantidade_registrada TEXT,
quantidade_empenhada TEXT,
saldo_empenho TEXT,
data_hora_inclusao TEXT,
data_hora_atualizacao TEXT,
data_hora_carga TIMESTAMPTZ DEFAULT now(),
PRIMARY KEY (numero_ata, unidade_gerenciadora, numero_item, unidade)
);
