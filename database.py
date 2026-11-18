"""
PEÇONHA+ - Banco de dados

Cria o banco SQLite e carrega os dados públicos das pastas data/.
Para recriar o banco do zero:  python database.py
"""
import csv
import json
import os
import sqlite3

PASTA = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_BANCO = os.path.join(PASTA, "peconha.db")

SOROS = [
    ("botropico", "Botrópico", "Jararaca"),
    ("crotalico", "Crotálico", "Cascavel"),
    ("elapidico", "Elapídico", "Coral-verdadeira"),
    ("laquetico", "Laquético", "Surucucu"),
    ("escorpionico", "Escorpiônico", "Escorpião"),
    ("loxoscelico", "Loxoscélico", "Aranha-marrom"),
    ("foneutrico", "Fonêutrico", "Armadeira"),
    ("lonomico", "Lonômico", "Taturana"),
]

# Nome do soro como aparece no PDF do Ministério da Saúde -> código no banco
NOME_PARA_CODIGO = {nome: codigo for codigo, nome, animal in SOROS}

# As unidades da capital ficam todas no mesmo município, então usamos
# a posição aproximada do bairro para não ficarem empilhadas no mapa.
POSICAO_CAPITAL = {
    "2077671": (-23.7745, -46.6745),  # Grajaú
    "2082225": (-23.4330, -46.7140),  # Taipas
    "6135927": (-23.8220, -46.7290),  # Parelheiros
    "2080346": (-23.5370, -46.5700),  # Tatuapé
    "2080583": (-23.4970, -46.4450),  # São Miguel Paulista
    "2091356": (-23.5655, -46.7185),  # Butantã
    "7479387": (-23.6400, -46.7600),  # Campo Limpo
}


def conectar():
    conexao = sqlite3.connect(ARQUIVO_BANCO)
    conexao.row_factory = sqlite3.Row  # permite acessar colunas pelo nome
    return conexao


def separar_soros(texto):
    """'Botrópico, Crotálico e Escorpiônico' -> ['botropico', 'crotalico', 'escorpionico']"""
    texto = texto.replace(" e ", ", ")
    codigos = []
    for nome in texto.split(","):
        nome = nome.strip()
        if nome:
            codigos.append(NOME_PARA_CODIGO[nome])
    return codigos


def criar_banco():
    conexao = conectar()
    cursor = conexao.cursor()

    # 1. Tabelas
    with open(os.path.join(PASTA, "schema.sql"), encoding="utf-8") as arquivo:
        cursor.executescript(arquivo.read())

    # 2. Soros
    cursor.executemany("INSERT INTO soro VALUES (?, ?, ?)", SOROS)

    # 3. Municípios de SP
    municipios = {}
    with open(os.path.join(PASTA, "data", "raw", "municipios_sp.csv"), encoding="utf-8") as arquivo:
        for linha in csv.DictReader(arquivo):
            municipios[linha["nome"]] = linha
            cursor.execute(
                "INSERT INTO municipio VALUES (?, ?, ?, ?)",
                (linha["codigo_ibge"], linha["nome"], linha["latitude"], linha["longitude"]),
            )

    # 4. Unidades de saúde com soro
    unidades_por_cidade = {}
    with open(os.path.join(PASTA, "data", "raw", "unidades_sp.csv"), encoding="utf-8") as arquivo:
        for linha in csv.DictReader(arquivo, delimiter=";"):
            cidade = municipios[linha["municipio"]]

            if linha["cnes"] in POSICAO_CAPITAL:
                lat, lon = POSICAO_CAPITAL[linha["cnes"]]
            else:
                # centro do município (unidades extras ficam um pouco deslocadas)
                n = unidades_por_cidade.get(linha["municipio"], 0)
                lat = float(cidade["latitude"]) + 0.006 * n
                lon = float(cidade["longitude"]) + 0.006 * n
            unidades_por_cidade[linha["municipio"]] = unidades_por_cidade.get(linha["municipio"], 0) + 1

            cursor.execute(
                """INSERT INTO unidade (nome, endereco, telefone, cnes, codigo_ibge, latitude, longitude)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (linha["unidade"], linha["endereco"], linha["telefone"], linha["cnes"],
                 cidade["codigo_ibge"], lat, lon),
            )
            unidade_id = cursor.lastrowid
            for codigo in separar_soros(linha["soros"]):
                cursor.execute("INSERT INTO unidade_soro VALUES (?, ?)", (unidade_id, codigo))

    # 5. Espécies
    with open(os.path.join(PASTA, "data", "especies.json"), encoding="utf-8") as arquivo:
        especies = json.load(arquivo)
    for e in especies:
        cursor.execute(
            "INSERT INTO especie VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (e["id"], e["nome"], e["cientifico"], e["grupo"], e["perigo"], e["soro"],
             e["descricao"], e["habitat"], e["sintomas"], e["prevencao"]),
        )

    conexao.commit()
    conexao.close()
    print("Banco criado com sucesso!")


if __name__ == "__main__":
    criar_banco()
