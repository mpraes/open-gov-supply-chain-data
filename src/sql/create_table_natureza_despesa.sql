CREATE TABLE material_natureza_despesa (
cod_pdm BIGINT NOT NULL REFERENCES material_pdm (cod_pdm),
cod_natureza_despesa varchar(50) NOT NULL,
nome_natureza_despesa varchar(200) NOT NULL,
status_natureza_despesa varchar(50),
data_hora_carga TIMESTAMPTZ DEFAULT now(),
PRIMARY KEY (cod_pdm, cod_natureza_despesa)
);
