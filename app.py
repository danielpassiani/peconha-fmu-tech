"""
PEÇONHA+ - Prevenção e Informação sobre Animais Peçonhentos
Projeto FMU Tech Inovação 2026.2 (ODS 3)

Para rodar:  python app.py   e abra http://localhost:5000
"""
import json
import math
import os
from datetime import date

from flask import Flask, abort, jsonify, redirect, render_template, request

from database import ARQUIVO_BANCO, PASTA, conectar, criar_banco

app = Flask(__name__)

# Animais que aparecem no fluxo de emergência
GRUPOS = {
    "escorpiao": {"nome": "Escorpião", "emoji": "🦂", "descricao": "Picada com dor forte"},
    "serpente": {"nome": "Cobra", "emoji": "🐍", "descricao": "Qualquer tipo de cobra"},
    "aranha": {"nome": "Aranha", "emoji": "🕷️", "descricao": "Marrom, armadeira..."},
    "lagarta": {"nome": "Lagarta", "emoji": "🐛", "descricao": "Taturana, lagarta com pelos"},
    "abelha": {"nome": "Abelha / vespa", "emoji": "🐝", "descricao": "Uma ou várias picadas"},
    "desconhecido": {"nome": "Não sei", "emoji": "❓", "descricao": "Não vi o animal"},
}

# Soros que a unidade precisa ter para atender cada caso
SOROS_POR_GRUPO = {
    "escorpiao": ["escorpionico"],
    "serpente": ["botropico", "crotalico"],    # jararaca e cascavel: as mais comuns
    "aranha": ["loxoscelico", "foneutrico"],   # aranha-marrom e armadeira
    "lagarta": ["lonomico"],
    "abelha": [],                              # não há soro de uso rotineiro
    "desconhecido": [],
}


def ler_json(nome_arquivo):
    with open(os.path.join(PASTA, "data", nome_arquivo), encoding="utf-8") as arquivo:
        return json.load(arquivo)


def calcular_distancia(lat1, lon1, lat2, lon2):
    """Distância em km entre dois pontos (fórmula de Haversine)."""
    raio_terra = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2
         + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    return raio_terra * 2 * math.asin(math.sqrt(a))


def buscar_unidades(soro=None, cidade=None):
    """Lista as unidades com os soros de cada uma. Pode filtrar por soro e por cidade."""
    conexao = conectar()
    sql = """
        SELECT u.id, u.nome, u.endereco, u.telefone, u.latitude, u.longitude,
               m.nome AS municipio, GROUP_CONCAT(us.soro_codigo) AS soros
        FROM unidade u
        JOIN municipio m ON m.codigo_ibge = u.codigo_ibge
        JOIN unidade_soro us ON us.unidade_id = u.id
        GROUP BY u.id
        ORDER BY m.nome, u.nome
    """
    linhas = conexao.execute(sql).fetchall()
    conexao.close()

    unidades = []
    for linha in linhas:
        unidade = dict(linha)
        unidade["soros"] = unidade["soros"].split(",")
        if soro and soro not in unidade["soros"]:
            continue
        if cidade and cidade.lower() not in unidade["municipio"].lower():
            continue
        unidades.append(unidade)
    return unidades


def nomes_dos_soros():
    conexao = conectar()
    linhas = conexao.execute("SELECT codigo, nome, animal FROM soro ORDER BY nome").fetchall()
    conexao.close()
    return {linha["codigo"]: dict(linha) for linha in linhas}


# ---------------------------------------------------------------- páginas

@app.route("/")
def inicio():
    conexao = conectar()
    total_unidades = conexao.execute("SELECT COUNT(*) FROM unidade").fetchone()[0]
    conexao.close()
    return render_template("index.html", total_unidades=total_unidades)


@app.route("/emergencia")
def emergencia():
    return render_template("emergencia.html", grupos=GRUPOS)


@app.route("/emergencia/<grupo>")
def emergencia_grupo(grupo):
    if grupo not in GRUPOS:
        abort(404)
    socorros = ler_json("primeiros_socorros.json")
    conexao = conectar()
    municipios = conexao.execute("SELECT nome, latitude, longitude FROM municipio ORDER BY nome").fetchall()
    conexao.close()
    return render_template(
        "primeiros_socorros.html",
        grupo=grupo,
        animal=GRUPOS[grupo],
        orientacao=socorros["grupos"][grupo],
        geral=socorros["geral"],
        contatos=socorros["contatos"],
        soros_necessarios=SOROS_POR_GRUPO[grupo],
        soros=nomes_dos_soros(),
        municipios=municipios,
    )


@app.route("/mapa")
def mapa():
    soro = request.args.get("soro", "")
    cidade = request.args.get("cidade", "").strip()
    unidades = buscar_unidades(soro, cidade)
    return render_template("mapa.html", unidades=unidades, soros=nomes_dos_soros(),
                           soro_escolhido=soro, cidade=cidade)


@app.route("/especies")
def especies():
    conexao = conectar()
    lista = conexao.execute("SELECT * FROM especie ORDER BY grupo, nome").fetchall()
    conexao.close()
    return render_template("especies.html", especies=lista, grupos=GRUPOS, soros=nomes_dos_soros())


@app.route("/especies/<id>")
def especie(id):
    conexao = conectar()
    item = conexao.execute("SELECT * FROM especie WHERE id = ?", (id,)).fetchone()
    conexao.close()
    if item is None:
        abort(404)
    return render_template("especie.html", e=item, grupos=GRUPOS, soros=nomes_dos_soros())


@app.route("/dados")
def dados():
    estatisticas = ler_json("estatisticas.json")
    escorpiao = estatisticas["escorpiao"]
    estados = sorted(escorpiao["por_uf"], key=lambda uf: uf["casos"], reverse=True)
    sp = next(uf for uf in estados if uf["uf"] == "SP")

    conexao = conectar()
    por_soro = conexao.execute("""
        SELECT s.nome, s.animal, COUNT(us.unidade_id) AS total
        FROM soro s LEFT JOIN unidade_soro us ON us.soro_codigo = s.codigo
        GROUP BY s.codigo ORDER BY total DESC
    """).fetchall()
    total_unidades = conexao.execute("SELECT COUNT(*) FROM unidade").fetchone()[0]
    total_cidades = conexao.execute("SELECT COUNT(DISTINCT codigo_ibge) FROM unidade").fetchone()[0]
    conexao.close()

    return render_template(
        "dados.html",
        e=escorpiao,
        fonte=estatisticas["fonte"],
        fonte_url=estatisticas["fonte_url"],
        estados=estados[:10],
        maior_estado=estados[0]["casos"],
        sp=sp,
        por_soro=por_soro,
        maior_soro=por_soro[0]["total"],
        total_unidades=total_unidades,
        total_cidades=total_cidades,
        maior_letalidade=max(f["letalidade"] for f in escorpiao["faixa_etaria"]),
    )


@app.route("/avistamentos", methods=["GET", "POST"])
def avistamentos():
    conexao = conectar()
    erro = None

    # Formulário enviado: valida e salva no banco
    if request.method == "POST":
        grupo = request.form.get("grupo", "")
        codigo_ibge = request.form.get("cidade", "")
        data = request.form.get("data", "")
        bairro = request.form.get("bairro", "").strip()
        observacao = request.form.get("observacao", "").strip()

        cidade_existe = conexao.execute(
            "SELECT 1 FROM municipio WHERE codigo_ibge = ?", (codigo_ibge,)
        ).fetchone()

        if grupo not in GRUPOS or grupo == "desconhecido":
            erro = "Escolha o animal que você viu."
        elif not cidade_existe:
            erro = "Escolha a cidade."
        elif not data or data > date.today().isoformat():
            erro = "Informe uma data válida (não pode ser no futuro)."
        else:
            conexao.execute(
                "INSERT INTO avistamento (grupo, codigo_ibge, data, bairro, observacao) VALUES (?, ?, ?, ?, ?)",
                (grupo, codigo_ibge, data, bairro[:80], observacao[:300]),
            )
            conexao.commit()
            conexao.close()
            return redirect("/avistamentos?ok=1")

    # Lista dos últimos avistamentos
    lista = conexao.execute("""
        SELECT a.grupo, a.data, a.bairro, a.observacao, m.nome AS cidade
        FROM avistamento a
        JOIN municipio m ON m.codigo_ibge = a.codigo_ibge
        ORDER BY a.data DESC, a.id DESC
        LIMIT 20
    """).fetchall()
    total = conexao.execute("SELECT COUNT(*) FROM avistamento").fetchone()[0]
    municipios = conexao.execute("SELECT codigo_ibge, nome FROM municipio ORDER BY nome").fetchall()
    conexao.close()

    animais = {codigo: g for codigo, g in GRUPOS.items() if codigo != "desconhecido"}
    return render_template(
        "avistamentos.html",
        lista=lista,
        total=total,
        municipios=municipios,
        animais=animais,
        hoje=date.today().isoformat(),
        erro=erro,
        sucesso=request.args.get("ok"),
    )


# ---------------------------------------------------------------- API (usada pelo JavaScript)

@app.route("/api/unidades/proximas")
def api_unidades_proximas():
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)
    grupo = request.args.get("grupo", "desconhecido")
    if lat is None or lon is None or grupo not in SOROS_POR_GRUPO:
        return jsonify({"erro": "Parâmetros inválidos"}), 400

    necessarios = SOROS_POR_GRUPO[grupo]
    resultado = []
    for unidade in buscar_unidades():
        # a unidade precisa ter TODOS os soros necessários
        if all(soro in unidade["soros"] for soro in necessarios):
            unidade["distancia_km"] = round(calcular_distancia(lat, lon, unidade["latitude"], unidade["longitude"]), 1)
            resultado.append(unidade)

    resultado.sort(key=lambda u: u["distancia_km"])
    return jsonify(resultado[:5])


@app.errorhandler(404)
def pagina_nao_encontrada(erro):
    return render_template("404.html"), 404


if __name__ == "__main__":
    if not os.path.exists(ARQUIVO_BANCO):
        criar_banco()
    app.run(debug=True)
