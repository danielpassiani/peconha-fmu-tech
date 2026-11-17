"""Inicia o PEÇONHA+ localmente: python run.py"""
import os

from app import create_app
from app.db import DEFAULT_DB_PATH
from app.seed import seed

if not DEFAULT_DB_PATH.exists():
    seed()

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
