"""Cria o banco e carrega os dados públicos.

Uso:  python -m app.seed
"""
import csv
import json
import re
import sys
import unicodedata
from pathlib import Path

from app.db import BASE_DIR, DEFAULT_DB_PATH, connect

DATA = BASE_DIR / "data"
RAW = DATA / "raw"

SOROS = [
    ("botropico", "Botrópico", "Jararaca"),
    ("crotalico", "Crotálico", "Cascavel"),
    ("elapidico", "Elapídico", "Coral-verdadeira"),
    ("laquetico", "Laquético", "Surucucu"),
    ("escorpionico", "Escorpiônico", "Escorpião"),
    ("loxoscelico", "Loxoscélico", "Aranha-marrom"),
    ("foneutrico", "Fonêutrico", "Armadeira"),
    ("lonomico", "Lonômico", "Taturana (Lonomia)"),
]

# Coordenadas aproximadas das unidades da capital (bairro), para não
# empilhar todas no centro do município.
COORDS_CAPITAL = {
    "2077671": (-23.7745, -46.6745),  # Grajaú
    "2082225": (-23.4330, -46.7140),  # Taipas
    "6135927": (-23.8220, -46.7290),  # Parelheiros
    "2080346": (-23.5370, -46.5700),  # Tatuapé
    "2080583": (-23.4970, -46.4450),  # São Miguel Paulista
    "2091356": (-23.5655, -46.7185),  # Butantã
    "7479387": (-23.6400, -46.7600),  # Campo Limpo
}


def sem_acento(texto):
    return "".join(c for c in unicodedata.normalize("NFD", texto) if unicodedata.category(c) != "Mn").lower()


def parse_soros(texto):
    """'Botrópico, Crotálico e Escorpiônico' -> ['botropico', 'crotalico', 'escorpionico']"""
    partes = re.split(r",|\be\b", sem_acento(texto))
    codigos = {p.strip().rstrip(".") for p in partes if p.strip()}
    validos = {c for c, _, _ in SOROS}
    desconhecidos = codigos - validos
    if desconhecidos:
        raise ValueError(f"Soro desconhecido: {desconhecidos} em '{texto}'")
    return sorted(codigos)


def seed(db_path=None, verbose=True):
    conn = connect(db_path or DEFAULT_DB_PATH)
    conn.executescript((Path(__file__).parent / "schema.sql").read_text(encoding="utf-8"))

    conn.executemany("INSERT INTO soro VALUES (?, ?, ?)", SOROS)

    # Municípios (IBGE)
    municipios = {}
    with open(RAW / "municipios_sp.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            municipios[r["nome"]] = r
            conn.execute(
                "INSERT INTO municipio (codigo_ibge, nome, latitude, longitude) VALUES (?, ?, ?, ?)",
                (int(r["codigo_ibge"]), r["nome"], float(r["latitude"]), float(r["longitude"])),
            )

    # Unidades com soro (Ministério da Saúde)
    por_municipio = {}
    total = 0
    with open(RAW / "unidades_sp.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter=";"):
            m = municipios.get(r["municipio"])
            if m is None:
                raise ValueError(f"Município não encontrado no IBGE: {r['municipio']}")
            n = por_municipio.get(r["municipio"], 0)
            por_municipio[r["municipio"]] = n + 1

            if r["cnes"] in COORDS_CAPITAL:
                lat, lon = COORDS_CAPITAL[r["cnes"]]
            else:
                # Centro do município; unidades extras levemente deslocadas
                lat = float(m["latitude"]) + 0.006 * n
                lon = float(m["longitude"]) + 0.006 * n

            cur = conn.execute(
                """INSERT INTO unidade (nome, endereco, telefone, cnes, codigo_municipio, latitude, longitude)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (r["unidade"], r["endereco"], r["telefone"], r["cnes"] or None,
                 int(m["codigo_ibge"]), lat, lon),
            )
            conn.executemany(
                "INSERT INTO unidade_soro VALUES (?, ?)",
                [(cur.lastrowid, s) for s in parse_soros(r["soros"])],
            )
            total += 1

    # Espécies
    especies = json.loads((DATA / "especies.json").read_text(encoding="utf-8"))
    for e in especies:
        conn.execute(
            """INSERT INTO especie (id, nome, cientifico, grupo, perigo, descricao, habitat, sintomas, prevencao)
               VALUES (:id, :nome, :cientifico, :grupo, :perigo, :descricao, :habitat, :sintomas, :prevencao)""",
            e,
        )
        conn.executemany("INSERT INTO especie_soro VALUES (?, ?)", [(e["id"], s) for s in e["soros"]])

    conn.commit()
    conn.close()
    if verbose:
        print(f"Banco criado: {len(municipios)} municípios, {total} unidades, {len(especies)} espécies.")


if __name__ == "__main__":
    seed(sys.argv[1] if len(sys.argv) > 1 else None)
