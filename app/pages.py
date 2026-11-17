"""Rotas das páginas (HTML)."""
from flask import Blueprint, render_template

pages = Blueprint("pages", __name__)


@pages.get("/")
def inicio():
    return render_template("inicio.html", ativo="inicio")


@pages.get("/emergencia")
def emergencia():
    return render_template("emergencia.html", ativo="emergencia")


@pages.get("/mapa")
def mapa():
    return render_template("mapa.html", ativo="mapa")


@pages.get("/especies")
def especies():
    return render_template("especies.html", ativo="especies")


@pages.get("/dados")
def dados():
    return render_template("dados.html", ativo="dados")
