-- PEÇONHA+ · modelo relacional (SQLite)

DROP TABLE IF EXISTS unidade_soro;
DROP TABLE IF EXISTS especie_soro;
DROP TABLE IF EXISTS unidade;
DROP TABLE IF EXISTS especie;
DROP TABLE IF EXISTS soro;
DROP TABLE IF EXISTS municipio;

CREATE TABLE municipio (
    codigo_ibge INTEGER PRIMARY KEY,
    nome        TEXT    NOT NULL,
    uf          TEXT    NOT NULL DEFAULT 'SP',
    latitude    REAL    NOT NULL,
    longitude   REAL    NOT NULL
);

-- Tipos de soro antiveneno distribuídos pelo Ministério da Saúde
CREATE TABLE soro (
    codigo    TEXT PRIMARY KEY,          -- ex.: 'botropico'
    nome      TEXT NOT NULL,             -- ex.: 'Botrópico'
    indicacao TEXT NOT NULL              -- ex.: 'Jararaca'
);

-- Pontos de atendimento com soro (lista oficial do Ministério da Saúde)
CREATE TABLE unidade (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    nome             TEXT    NOT NULL,
    endereco         TEXT,
    telefone         TEXT,
    cnes             TEXT,
    codigo_municipio INTEGER NOT NULL REFERENCES municipio(codigo_ibge),
    latitude         REAL    NOT NULL,
    longitude        REAL    NOT NULL,
    localizacao_aproximada INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE unidade_soro (
    unidade_id  INTEGER NOT NULL REFERENCES unidade(id) ON DELETE CASCADE,
    soro_codigo TEXT    NOT NULL REFERENCES soro(codigo),
    PRIMARY KEY (unidade_id, soro_codigo)
);

CREATE TABLE especie (
    id         TEXT PRIMARY KEY,
    nome       TEXT NOT NULL,
    cientifico TEXT NOT NULL,
    grupo      TEXT NOT NULL CHECK (grupo IN ('escorpiao','serpente','aranha','lagarta','abelha')),
    perigo     TEXT NOT NULL CHECK (perigo IN ('baixo','medio','alto')),
    descricao  TEXT,
    habitat    TEXT,
    sintomas   TEXT,
    prevencao  TEXT
);

CREATE TABLE especie_soro (
    especie_id  TEXT NOT NULL REFERENCES especie(id) ON DELETE CASCADE,
    soro_codigo TEXT NOT NULL REFERENCES soro(codigo),
    PRIMARY KEY (especie_id, soro_codigo)
);

CREATE INDEX idx_unidade_municipio ON unidade(codigo_municipio);
CREATE INDEX idx_unidade_soro_soro ON unidade_soro(soro_codigo);
