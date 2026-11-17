"""API REST do PEÇONHA+."""
import json
import math

from flask import Blueprint, abort, jsonify, request

from app.db import BASE_DIR, get_db

api = Blueprint("api", __name__)

DATA = BASE_DIR / "data"
GRUPOS = {"escorpiao", "serpente", "aranha", "lagarta", "abelha", "desconhecido"}


def carregar_json(nome):
    return json.loads((DATA / nome).read_text(encoding="utf-8"))


def distancia_km(lat1, lon1, lat2, lon2):
    """Distância em linha reta (fórmula de Haversine)."""
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def listar_unidades(soros=None, municipio=None):
    """Unidades com a lista de soros. Se `soros` for informado, só as que têm TODOS eles."""
    db = get_db()
    sql = """
        SELECT u.id, u.nome, u.endereco, u.telefone, u.cnes, u.latitude, u.longitude,
               u.localizacao_aproximada, m.nome AS municipio, m.codigo_ibge,
               GROUP_CONCAT(us.soro_codigo) AS soros
        FROM unidade u
        JOIN municipio m ON m.codigo_ibge = u.codigo_municipio
        JOIN unidade_soro us ON us.unidade_id = u.id
    """
    params = []
    if municipio:
        sql += " WHERE m.codigo_ibge = ?"
        params.append(municipio)
    sql += " GROUP BY u.id ORDER BY m.nome, u.nome"

    unidades = []
    for row in db.execute(sql, params):
        u = dict(row)
        u["soros"] = sorted(u["soros"].split(","))
        u["localizacao_aproximada"] = bool(u["localizacao_aproximada"])
        if soros and not set(soros) <= set(u["soros"]):
            continue
        unidades.append(u)
    return unidades


def parse_soros_param():
    valor = request.args.get("soro", "").strip()
    if not valor:
        return []
    soros = [s.strip() for s in valor.split(",") if s.strip()]
    validos = {r["codigo"] for r in get_db().execute("SELECT codigo FROM soro")}
    invalidos = set(soros) - validos
    if invalidos:
        abort(400, description=f"Soro inválido: {', '.join(sorted(invalidos))}")
    return soros


@api.errorhandler(400)
@api.errorhandler(404)
def erro_json(e):
    return jsonify(erro=e.description), e.code


@api.get("/soros")
def soros():
    rows = get_db().execute("SELECT codigo, nome, indicacao FROM soro ORDER BY nome")
    return jsonify([dict(r) for r in rows])


@api.get("/municipios")
def municipios():
    rows = get_db().execute(
        """SELECT m.codigo_ibge, m.nome, m.latitude, m.longitude, COUNT(u.id) AS unidades
           FROM municipio m LEFT JOIN unidade u ON u.codigo_municipio = m.codigo_ibge
           GROUP BY m.codigo_ibge ORDER BY m.nome"""
    )
    return jsonify([dict(r) for r in rows])


@api.get("/unidades")
def unidades():
    municipio = request.args.get("municipio", type=int)
    return jsonify(listar_unidades(parse_soros_param(), municipio))


@api.get("/unidades/proximas")
def unidades_proximas():
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)
    if lat is None or lon is None:
        abort(400, description="Informe lat e lon.")
    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
        abort(400, description="Coordenadas inválidas.")
    limite = max(1, min(request.args.get("limite", default=5, type=int), 20))

    resultado = listar_unidades(parse_soros_param())
    for u in resultado:
        u["distancia_km"] = round(distancia_km(lat, lon, u["latitude"], u["longitude"]), 1)
    resultado.sort(key=lambda u: u["distancia_km"])
    return jsonify(resultado[:limite])


@api.get("/especies")
def especies():
    db = get_db()
    grupo = request.args.get("grupo")
    sql = "SELECT * FROM especie"
    params = []
    if grupo:
        sql += " WHERE grupo = ?"
        params.append(grupo)
    sql += " ORDER BY grupo, nome"
    lista = []
    for row in db.execute(sql, params):
        e = dict(row)
        e["soros"] = [r["soro_codigo"] for r in db.execute(
            "SELECT soro_codigo FROM especie_soro WHERE especie_id = ?", (e["id"],))]
        lista.append(e)
    return jsonify(lista)


@api.get("/especies/<especie_id>")
def especie(especie_id):
    db = get_db()
    row = db.execute("SELECT * FROM especie WHERE id = ?", (especie_id,)).fetchone()
    if row is None:
        abort(404, description="Espécie não encontrada.")
    e = dict(row)
    e["soros"] = [r["soro_codigo"] for r in db.execute(
        "SELECT soro_codigo FROM especie_soro WHERE especie_id = ?", (especie_id,))]
    return jsonify(e)


@api.get("/primeiros-socorros")
def primeiros_socorros_geral():
    return jsonify(carregar_json("primeiros_socorros.json"))


@api.get("/primeiros-socorros/<grupo>")
def primeiros_socorros(grupo):
    if grupo not in GRUPOS:
        abort(404, description="Grupo não encontrado.")
    dados = carregar_json("primeiros_socorros.json")
    return jsonify({
        "grupo": grupo,
        **dados["grupos"][grupo],
        **dados["geral"],
        "contatos": dados["contatos"],
        "fonte": dados["fonte"],
    })


@api.get("/estatisticas")
def estatisticas():
    dados = carregar_json("estatisticas.json")
    db = get_db()
    dados["rede_sp"] = {
        "unidades": db.execute("SELECT COUNT(*) FROM unidade").fetchone()[0],
        "municipios_atendidos": db.execute(
            "SELECT COUNT(DISTINCT codigo_municipio) FROM unidade").fetchone()[0],
        "por_soro": [dict(r) for r in db.execute(
            """SELECT s.nome, COUNT(us.unidade_id) AS unidades
               FROM soro s LEFT JOIN unidade_soro us ON us.soro_codigo = s.codigo
               GROUP BY s.codigo ORDER BY unidades DESC""")],
    }
    return jsonify(dados)
