"""Testes da API do PEÇONHA+.  Rodar com:  python -m pytest"""
import pytest

from app import create_app
from app.api import distancia_km
from app.seed import parse_soros, seed


@pytest.fixture(scope="session")
def client(tmp_path_factory):
    db_path = tmp_path_factory.mktemp("db") / "teste.db"
    seed(db_path, verbose=False)
    app = create_app({"DATABASE": str(db_path), "TESTING": True})
    return app.test_client()


def test_parse_soros():
    assert parse_soros("Botrópico, Crotálico e Escorpiônico") == ["botropico", "crotalico", "escorpionico"]
    with pytest.raises(ValueError):
        parse_soros("Inexistente")


def test_distancia_km():
    # São Paulo (Sé) -> Campinas: ~84 km em linha reta
    assert 80 < distancia_km(-23.5505, -46.6333, -22.9056, -47.0608) < 90


def test_paginas_carregam(client):
    for rota in ["/", "/emergencia", "/mapa", "/especies", "/dados"]:
        assert client.get(rota).status_code == 200


def test_unidades_filtradas_por_soro(client):
    dados = client.get("/api/unidades?soro=laquetico").get_json()
    assert dados, "deve existir ao menos uma unidade com soro laquético"
    assert all("laquetico" in u["soros"] for u in dados)


def test_unidades_proximas_ordenadas(client):
    # Instituto Butantan: a unidade mais próxima deve ser o Hospital Vital Brazil
    dados = client.get("/api/unidades/proximas?lat=-23.566&lon=-46.719&soro=elapidico").get_json()
    assert "Vital Brazil" in dados[0]["nome"]
    distancias = [u["distancia_km"] for u in dados]
    assert distancias == sorted(distancias)


def test_unidades_proximas_valida_parametros(client):
    assert client.get("/api/unidades/proximas").status_code == 400
    assert client.get("/api/unidades/proximas?lat=-23&lon=-46&soro=xyz").status_code == 400


def test_primeiros_socorros(client):
    d = client.get("/api/primeiros-socorros/escorpiao").get_json()
    assert d["soros"] == ["escorpionico"]
    assert any("torniquete" in item for item in d["nao_faca"])
    assert client.get("/api/primeiros-socorros/dragao").status_code == 404


def test_especies(client):
    lista = client.get("/api/especies").get_json()
    assert len(lista) >= 10
    assert client.get("/api/especies/jararaca").get_json()["soros"] == ["botropico"]
    assert client.get("/api/especies/nao-existe").status_code == 404


def test_estatisticas(client):
    d = client.get("/api/estatisticas").get_json()
    assert sum(u["casos"] for u in d["escorpiao"]["por_uf"]) == d["escorpiao"]["casos"]
    assert d["rede_sp"]["unidades"] > 100
