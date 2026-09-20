CREATE TABLE arp_adesao (
numero_ata TEXT NOT NULL,
unidade_gerenciadora TEXT NOT NULL,
unidade_nao_participante TEXT NOT NULL,
data_aprovacao_analise TEXT,
quantidade_aprovada_adesao TEXT,
data_hora_carga TIMESTAMPTZ DEFAULT now(),
PRIMARY KEY (numero_ata, unidade_gerenciadora, unidade_nao_participante)
);
