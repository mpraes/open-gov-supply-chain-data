CREATE TABLE indicador_periodo (
ano_mes TEXT NOT NULL,
ano TEXT,
mes TEXT,
total_servicos TEXT,
total_requisicoes TEXT,
percentual_sucesso TEXT,
media_tempo_resposta_ms TEXT,
total_download_gb TEXT,
total_download_mbytes TEXT,
data_hora_carga TIMESTAMPTZ DEFAULT now(),
PRIMARY KEY (ano_mes)
);
