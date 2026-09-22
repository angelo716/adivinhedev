from flask import Flask, jsonify, request, send_from_directory, Response
from pathlib import Path
from functools import wraps
import sqlite3
import time
import os
import hmac

app = Flask(__name__)

PASTA_DO_JOGO = Path(__file__).resolve().parent
ARQUIVO_BANCO = PASTA_DO_JOGO / "jogo.db"

USUARIO_ADMIN = os.environ.get("USUARIO_ADMIN", "admin")
SENHA_ADMIN = os.environ.get("SENHA_ADMIN")


def conectar_banco():
    conexao = sqlite3.connect(ARQUIVO_BANCO)
    conexao.row_factory = sqlite3.Row
    return conexao


def criar_banco():
    with conectar_banco() as banco:
        banco.execute("""
            CREATE TABLE IF NOT EXISTS estatisticas (
                id INTEGER PRIMARY KEY,
                vitorias INTEGER NOT NULL DEFAULT 0,
                derrotas INTEGER NOT NULL DEFAULT 0
            )
        """)

        banco.execute("""
            CREATE TABLE IF NOT EXISTS jogadores_online (
                jogador_id TEXT PRIMARY KEY,
                ultimo_ping REAL NOT NULL
            )
        """)

        banco.execute("""
            INSERT OR IGNORE INTO estatisticas (id, vitorias, derrotas)
            VALUES (1, 0, 0)
        """)


def limpar_jogadores_offline(banco):
    limite = time.time() - 30

    banco.execute(
        "DELETE FROM jogadores_online WHERE ultimo_ping < ?",
        (limite,)
    )


def pedir_senha():
    return Response(
        "Acesso restrito.",
        401,
        {"WWW-Authenticate": 'Basic realm="Painel Admin"'}
    )


def exige_admin(funcao):
    @wraps(funcao)
    def protegida(*args, **kwargs):
        login = request.authorization

        if not login or not SENHA_ADMIN:
            return pedir_senha()

        usuario_certo = hmac.compare_digest(
            login.username,
            USUARIO_ADMIN
        )

        senha_certa = hmac.compare_digest(
            login.password,
            SENHA_ADMIN
        )

        if not usuario_certo or not senha_certa:
            return pedir_senha()

        return funcao(*args, **kwargs)

    return protegida


@app.route("/")
def inicio():
    return send_from_directory(PASTA_DO_JOGO, "index.html")


@app.route("/style.css")
def estilo():
    return send_from_directory(PASTA_DO_JOGO, "style.css")


@app.route("/admin")
@exige_admin
def admin():
    return send_from_directory(PASTA_DO_JOGO, "admin.html")


@app.route("/api/online", methods=["POST"])
def registrar_online():
    dados = request.get_json(silent=True) or {}
    jogador_id = dados.get("jogador_id")

    if not jogador_id:
        return jsonify({"erro": "Jogador inválido."}), 400

    with conectar_banco() as banco:
        limpar_jogadores_offline(banco)

        banco.execute("""
            INSERT INTO jogadores_online (jogador_id, ultimo_ping)
            VALUES (?, ?)
            ON CONFLICT(jogador_id)
            DO UPDATE SET ultimo_ping = excluded.ultimo_ping
        """, (jogador_id, time.time()))

        online = banco.execute(
            "SELECT COUNT(*) AS total FROM jogadores_online"
        ).fetchone()["total"]

    return jsonify({"online": online})


@app.route("/api/resultado", methods=["POST"])
def registrar_resultado():
    dados = request.get_json(silent=True) or {}
    resultado = dados.get("resultado")

    if resultado not in ["vitoria", "derrota"]:
        return jsonify({"erro": "Resultado inválido."}), 400

    coluna = "vitorias" if resultado == "vitoria" else "derrotas"

    with conectar_banco() as banco:
        banco.execute(
            f"UPDATE estatisticas SET {coluna} = {coluna} + 1 WHERE id = 1"
        )

    return jsonify({"ok": True})


@app.route("/api/estatisticas")
@exige_admin
def estatisticas():
    with conectar_banco() as banco:
        limpar_jogadores_offline(banco)

        dados = banco.execute("""
            SELECT vitorias, derrotas
            FROM estatisticas
            WHERE id = 1
        """).fetchone()

        online = banco.execute(
            "SELECT COUNT(*) AS total FROM jogadores_online"
        ).fetchone()["total"]

    return jsonify({
        "vitorias": dados["vitorias"],
        "derrotas": dados["derrotas"],
        "online": online
    })


criar_banco()

if __name__ == "__main__":
    app.run(debug=True)