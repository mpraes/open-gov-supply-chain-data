CREATE TABLE indicador_consolidado (
ano_mes_inicio TEXT NOT NULL,
ano_mes_fim TEXT NOT NULL,
total_servicos TEXT,
total_requisicoes TEXT,
percentual_sucesso TEXT,
media_tempo_resposta_ms TEXT,
total_download_gb TEXT,
media_download_mes_gb TEXT,
data_hora_carga TIMESTAMPTZ DEFAULT now(),
PRIMARY KEY (ano_mes_inicio, ano_mes_fim)
);
