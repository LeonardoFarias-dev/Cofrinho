import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("cofrinho.db")

def conectar():
    conexao = sqlite3.connect(DB_PATH)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao
