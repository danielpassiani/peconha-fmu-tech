-- PEÇONHA+ - Banco de dados (SQLite)

DROP TABLE IF EXISTS avistamento;
DROP TABLE IF EXISTS unidade_soro;
DROP TABLE IF EXISTS unidade;
DROP TABLE IF EXISTS especie;
DROP TABLE IF EXISTS soro;
DROP TABLE IF EXISTS municipio;

-- Municípios do estado de São Paulo (IBGE)
CREATE TABLE municipio (
    codigo_ibge INTEGER PRIMARY KEY,
    nome        TEXT NOT NULL,
    latitude    REAL NOT NULL,
    longitude   REAL NOT NULL
);

-- Tipos de soro antiveneno
CREATE TABLE soro (
    codigo TEXT PRIMARY KEY,   -- ex.: escorpionico
    nome   TEXT NOT NULL,      -- ex.: Escorpiônico
    animal TEXT NOT NULL       -- ex.: Escorpião
);

-- Unidades de saúde com soro (lista do Ministério da Saúde)
CREATE TABLE unidade (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    nome         TEXT NOT NULL,
    endereco     TEXT,
    telefone     TEXT,
    cnes         TEXT,
    codigo_ibge  INTEGER NOT NULL,
    latitude     REAL NOT NULL,
    longitude    REAL NOT NULL,
    FOREIGN KEY (codigo_ibge) REFERENCES municipio (codigo_ibge)
);

-- Quais soros cada unidade tem (relacionamento N:N)
CREATE TABLE unidade_soro (
    unidade_id  INTEGER NOT NULL,
    soro_codigo TEXT NOT NULL,
    PRIMARY KEY (unidade_id, soro_codigo),
    FOREIGN KEY (unidade_id) REFERENCES unidade (id),
    FOREIGN KEY (soro_codigo) REFERENCES soro (codigo)
);

-- Catálogo de espécies
CREATE TABLE especie (
    id          TEXT PRIMARY KEY,
    nome        TEXT NOT NULL,
    cientifico  TEXT NOT NULL,
    grupo       TEXT NOT NULL,   -- escorpiao, serpente, aranha, lagarta, abelha
    perigo      TEXT NOT NULL,   -- alto, medio
    soro_codigo TEXT,            -- soro indicado (vazio se não houver)
    descricao   TEXT,
    habitat     TEXT,
    sintomas    TEXT,
    prevencao   TEXT,
    FOREIGN KEY (soro_codigo) REFERENCES soro (codigo)
);

-- Avistamentos registrados pela comunidade
CREATE TABLE avistamento (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    grupo       TEXT NOT NULL,      -- escorpiao, serpente, aranha, lagarta, abelha
    codigo_ibge INTEGER NOT NULL,   -- cidade onde o animal foi visto
    data        TEXT NOT NULL,      -- data do avistamento (AAAA-MM-DD)
    bairro      TEXT,
    observacao  TEXT,
    criado_em   TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (codigo_ibge) REFERENCES municipio (codigo_ibge)
);
