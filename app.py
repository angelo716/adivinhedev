from flask import Flask, request, render_template_string, session, redirect, make_response
import random
import sqlite3
from pathlib import Path
import os
import uuid

app = Flask(__name__)
app.secret_key = "adivinhedev-chave-secreta"

BANCO = Path(__file__).with_name("ranking.db")

ADMIN_SENHA = os.environ.get("ADMIN_SENHA", "adivinhedev-admin")


# =========================================================
# BANCO DE DADOS
# =========================================================

def conectar():
    conexao = sqlite3.connect(BANCO)
    conexao.row_factory = sqlite3.Row
    return conexao


def criar_banco():
    with conectar() as conexao:

        conexao.execute("""
            CREATE TABLE IF NOT EXISTS pontuacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL COLLATE NOCASE,
                pontuacao INTEGER NOT NULL,
                tentativas INTEGER NOT NULL,
                resultado TEXT NOT NULL,
                data DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conexao.execute("""
            CREATE TABLE IF NOT EXISTS visitas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                visitante_id TEXT UNIQUE NOT NULL,
                primeira_visita DATETIME DEFAULT CURRENT_TIMESTAMP,
                ultima_visita DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)


def salvar_pontuacao(nome, pontuacao, tentativas, resultado):
    with conectar() as conexao:
        conexao.execute("""
            INSERT INTO pontuacoes
            (nome, pontuacao, tentativas, resultado)
            VALUES (?, ?, ?, ?)
        """, (nome, pontuacao, tentativas, resultado))


def buscar_ranking():
    with conectar() as conexao:
        return conexao.execute("""
            SELECT nome, MAX(pontuacao) AS melhor
            FROM pontuacoes
            WHERE resultado = 'Vitoria'
            GROUP BY nome COLLATE NOCASE
            ORDER BY melhor DESC, nome COLLATE NOCASE ASC
            LIMIT 10
        """).fetchall()


def buscar_historico(nome):
    with conectar() as conexao:
        return conexao.execute("""
            SELECT pontuacao, tentativas, resultado, data
            FROM pontuacoes
            WHERE nome = ? COLLATE NOCASE
            ORDER BY id DESC
        """, (nome,)).fetchall()


# =========================================================
# HTML DO JOGO
# =========================================================

HTML = """
<!DOCTYPE html>
<html lang="pt-br">

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>AdivinheDev 🎮</title>

    <style>

        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            min-height: 100vh;
            padding: 20px;
            font-family: Arial, sans-serif;
            background: linear-gradient(
                135deg,
                #2563eb,
                #1e3a8a
            );
        }

        .container {
            width: 100%;
            max-width: 900px;
            margin: auto;
        }

        .card {
            background: white;
            border-radius: 25px;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,.25);
            margin-bottom: 25px;
        }

        h1 {
            text-align: center;
            margin-top: 0;
            color: #111827;
        }

        h2 {
            color: #111827;
        }

        .subtitulo {
            text-align: center;
            color: #6b7280;
        }

        input {
            width: 100%;
            padding: 15px;
            border: 2px solid #d1d5db;
            border-radius: 12px;
            font-size: 18px;
            margin: 8px 0;
        }

        button {
            width: 100%;
            padding: 15px;
            border: none;
            border-radius: 12px;
            background: #2563eb;
            color: white;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            margin-top: 10px;
        }

        button:hover {
            background: #1d4ed8;
        }

        .mensagem {
            margin-top: 20px;
            padding: 18px;
            border-radius: 15px;
            background: #eff6ff;
            text-align: center;
            font-size: 20px;
            font-weight: bold;
        }

        .tentativas {
            text-align: center;
            margin-top: 15px;
            font-weight: bold;
        }

        .numero {
            text-align: center;
            font-size: 50px;
            margin: 15px 0;
        }

        .ranking {
            margin-top: 20px;
        }

        .linha {
            display: flex;
            justify-content: space-between;
            gap: 10px;
            padding: 12px;
            margin: 8px 0;
            border-radius: 10px;
            background: #f3f4f6;
        }

        .historico {
            overflow-x: auto;
        }

        table {
            width: 100%;
            border-collapse: collapse;
        }

        th,
        td {
            padding: 10px;
            border-bottom: 1px solid #ddd;
            text-align: center;
        }

        th {
            background: #f3f4f6;
        }

        .vitoria {
            color: #16a34a;
            font-weight: bold;
        }

        .derrota {
            color: #dc2626;
            font-weight: bold;
        }

        .novo-jogo {
            background: #111827;
        }

        .admin-link {
            display: block;
            text-align: center;
            margin-top: 15px;
            color: #6b7280;
            text-decoration: none;
            font-size: 13px;
        }

        @media (max-width: 600px) {

            body {
                padding: 10px;
            }

            .card {
                padding: 20px 15px;
                border-radius: 18px;
            }

            .numero {
                font-size: 40px;
            }

        }

    </style>

</head>

<body>

<div class="container">

    <div class="card">

        <h1>🎮 AdivinheDev</h1>

        <p class="subtitulo">
            Adivinhe o número secreto entre 1 e 100!
        </p>

        {% if not iniciado %}

            <form method="POST">

                <input
                    type="text"
                    name="nome"
                    placeholder="Digite seu nome"
                    maxlength="30"
                    required
                    autofocus
                >

                <button type="submit">
                    Começar jogo 🚀
                </button>

            </form>

        {% else %}

            <h2>
                Olá, {{ nome }}! 👋
            </h2>

            {% if not finalizado %}

                <div class="numero">
                    🤔
                </div>

                <form method="POST">

                    <input
                        type="number"
                        name="palpite"
                        min="1"
                        max="100"
                        placeholder="Digite seu palpite"
                        required
                        autofocus
                    >

                    <button type="submit">
                        Chutar 🎯
                    </button>

                </form>

            {% else %}

                <div class="numero">
                    {% if eficiencia > 0 %}
                        🏆
                    {% else %}
                        💀
                    {% endif %}
                </div>

            {% endif %}

            {% if mensagem %}

                <div class="mensagem">
                    {{ mensagem }}
                </div>

            {% endif %}

            <div class="tentativas">

                Tentativas:
                {{ tentativas }} / 10

                {% if finalizado %}

                    <br><br>

                    Eficiência:
                    {{ eficiencia }}%

                {% endif %}

            </div>

            {% if finalizado %}

                <form method="POST">

                    <button
                        class="novo-jogo"
                        type="submit"
                        name="novo_jogo"
                        value="1"
                    >
                        🔄 Novo jogo
                    </button>

                </form>

            {% endif %}

        {% endif %}

    </div>


    {% if ranking %}

    <div class="card ranking">

        <h2>🏆 Ranking</h2>

        {% for jogador in ranking %}

            <div class="linha">

                <strong>
                    {{ loop.index }}º
                    {{ jogador["nome"] }}
                </strong>

                <span>
                    {{ jogador["melhor"] }}%
                </span>

            </div>

        {% endfor %}

    </div>

    {% endif %}


    {% if iniciado and historico %}

    <div class="card historico">

        <h2>📜 Seu histórico</h2>

        <table>

            <tr>
                <th>Pontos</th>
                <th>Tentativas</th>
                <th>Resultado</th>
                <th>Data</th>
            </tr>

            {% for partida in historico %}

            <tr>

                <td>
                    {{ partida["pontuacao"] }}%
                </td>

                <td>
                    {{ partida["tentativas"] }}
                </td>

                <td>

                    {% if partida["resultado"] == "Vitoria" %}

                        <span class="vitoria">
                            🏆 Vitória
                        </span>

                    {% else %}

                        <span class="derrota">
                            💀 Derrota
                        </span>

                    {% endif %}

                </td>

                <td>
                    {{ partida["data"] }}
                </td>

            </tr>

            {% endfor %}

        </table>

    </div>

    {% endif %}

    <a
        class="admin-link"
        href="/admin"
    >
        🔐 Área administrativa
    </a>

</div>


<script>

    function tocarErro() {

        try {

            const audio =
                new AudioContext();

            const oscilador =
                audio.createOscillator();

            const ganho =
                audio.createGain();

            oscilador.frequency.value = 180;

            oscilador.connect(ganho);

            ganho.connect(audio.destination);

            oscilador.start();

            ganho.gain.exponentialRampToValueAtTime(
                0.001,
                audio.currentTime + 0.25
            );

            oscilador.stop(
                audio.currentTime + 0.25
            );

        } catch (e) {}

    }

</script>

</body>

</html>
"""


# =========================================================
# JOGO
# =========================================================

@app.route("/", methods=["GET", "POST"])
def inicio():

    visitor_id = request.cookies.get("visitor_id")

    if not visitor_id:
        visitor_id = str(uuid.uuid4())

    with conectar() as conexao:
        conexao.execute("""
            INSERT INTO visitas (visitante_id)
            VALUES (?)
            ON CONFLICT(visitante_id)
            DO UPDATE SET ultima_visita = CURRENT_TIMESTAMP
        """, (visitor_id,))

    if request.method == "POST" and "nome" in request.form:

        nome = request.form["nome"].strip()

        if nome:

            session.clear()

            session["nome"] = nome[:30]
            session["numero"] = random.randint(1, 100)
            session["tentativas"] = 0
            session["palpites"] = []
            session["mensagem"] = ""
            session["finalizado"] = False
            session["eficiencia"] = 0
            session["resultado"] = ""
            session["salvo"] = False

    elif request.method == "POST" and "novo_jogo" in request.form:

        session.clear()

    elif request.method == "POST" and "palpite" in request.form:

        if "nome" in session and not session.get(
            "finalizado",
            False
        ):

            try:
                palpite = int(
                    request.form["palpite"]
                )

            except (ValueError, TypeError):

                palpite = 0

            if palpite < 1 or palpite > 100:

                session["mensagem"] = (
                    "⚠️ Digite um número entre 1 e 100!"
                )

                session["resultado"] = ""

            else:

                palpites = session.get(
                    "palpites",
                    []
                )

                if palpite in palpites:

                    session["mensagem"] = (
                        "⚠️ Você já tentou esse número!"
                    )

                    session["resultado"] = ""

                else:

                    palpites.append(palpite)

                    session["palpites"] = palpites

                    session["tentativas"] += 1

                    numero = session["numero"]

                    tentativas = session["tentativas"]

                    if palpite == numero:

                        eficiencia = max(
                            10,
                            110 - (tentativas * 10)
                        )

                        session["eficiencia"] = eficiencia

                        session["mensagem"] = (
                            f"🎉 PARABÉNS, "
                            f"{session['nome']}! "
                            f"Você acertou o número!"
                        )

                        session["finalizado"] = True

                        session["resultado"] = "acerto"

                    elif palpite < numero:

                        session["mensagem"] = (
                            "📈 O número é MAIOR!"
                        )

                        session["resultado"] = "erro"

                    else:

                        session["mensagem"] = (
                            "📉 O número é MENOR!"
                        )

                        session["resultado"] = "erro"

                    if (
                        tentativas >= 10
                        and palpite != numero
                    ):

                        session["mensagem"] = (
                            f"💀 Fim de jogo! "
                            f"O número era {numero}."
                        )

                        session["eficiencia"] = 0

                        session["finalizado"] = True

                    if (
                        session["finalizado"]
                        and not session.get(
                            "salvo",
                            False
                        )
                    ):

                        if palpite == numero:

                            resultado = "Vitoria"

                        else:

                            resultado = "Derrota"

                        salvar_pontuacao(
                            session["nome"],
                            session["eficiencia"],
                            tentativas,
                            resultado
                        )

                        session["salvo"] = True

    iniciado = "nome" in session

    ranking = buscar_ranking()

    historico = (
        buscar_historico(
            session["nome"]
        )
        if iniciado
        else []
    )

    resposta = make_response(
        render_template_string(
            HTML,
            iniciado=iniciado,
            nome=session.get("nome", ""),
            tentativas=session.get(
                "tentativas",
                0
            ),
            mensagem=session.get(
                "mensagem",
                ""
            ),
            finalizado=session.get(
                "finalizado",
                False
            ),
            eficiencia=session.get(
                "eficiencia",
                0
            ),
            resultado=session.get(
                "resultado",
                ""
            ),
            ranking=ranking,
            historico=historico
        )
    )

    if not request.cookies.get("visitor_id"):

        resposta.set_cookie(
            "visitor_id",
            visitor_id,
            max_age=60 * 60 * 24 * 365 * 2,
            httponly=True,
            samesite="Lax"
        )

    return resposta


# =========================================================
# ADMIN - LOGIN
# =========================================================

HTML_ADMIN_LOGIN = """
<!DOCTYPE html>
<html lang="pt-br">

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>Admin - AdivinheDev</title>

    <style>

        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            min-height: 100vh;
            padding: 20px;
            font-family: Arial, sans-serif;
            background: linear-gradient(
                135deg,
                #111827,
                #2563eb
            );
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .caixa {
            width: 100%;
            max-width: 450px;
            background: white;
            border-radius: 25px;
            padding: 35px 25px;
            text-align: center;
            box-shadow: 0 20px 60px rgba(0,0,0,.35);
        }

        h1 {
            margin-top: 0;
        }

        input {
            width: 100%;
            padding: 15px;
            margin: 15px 0;
            font-size: 18px;
            border: 2px solid #aaa;
            border-radius: 12px;
        }

        button {
            padding: 14px 25px;
            font-size: 18px;
            border: none;
            border-radius: 12px;
            background: #2563eb;
            color: white;
            cursor: pointer;
        }

        .erro {
            color: #dc2626;
            font-weight: bold;
        }

    </style>

</head>

<body>

<div class="caixa">

    <h1>🔐 Painel Admin</h1>

    <p>AdivinheDev 🎮</p>

    {% if erro %}

        <p class="erro">
            ❌ Senha incorreta!
        </p>

    {% endif %}

    <form method="POST">

        <input
            type="password"
            name="senha"
            placeholder="Senha"
            required
            autofocus
        >

        <br>

        <button type="submit">
            Entrar 🔑
        </button>

    </form>

</div>

</body>

</html>
"""


# =========================================================
# ADMIN - PAINEL
# =========================================================

HTML_ADMIN = """
<!DOCTYPE html>
<html lang="pt-br">

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>Painel Admin - AdivinheDev</title>

    <style>

        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            min-height: 100vh;
            padding: 25px 12px;
            font-family: Arial, sans-serif;
            background: linear-gradient(
                135deg,
                #111827,
                #2563eb
            );
        }

        .caixa {
            width: 100%;
            max-width: 950px;
            margin: auto;
            background: white;
            border-radius: 25px;
            padding: 35px;
            box-shadow: 0 20px 60px rgba(0,0,0,.35);
        }

        h1 {
            text-align: center;
            margin-top: 0;
        }

        .subtitulo {
            text-align: center;
            color: #555;
        }

        .estatisticas {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 18px;
            margin-top: 30px;
        }

        .card {
            padding: 25px;
            border-radius: 18px;
            background: #f3f4f6;
            text-align: center;
        }

        .icone {
            font-size: 35px;
        }

        .numero {
            font-size: 35px;
            font-weight: bold;
            margin-top: 8px;
        }

        .nome {
            color: #555;
            margin-top: 5px;
        }

        .online {
            background: #ecfdf5;
        }

        .voltar {
            display: block;
            width: fit-content;
            margin: 30px auto 0;
            padding: 13px 22px;
            background: #2563eb;
            color: white;
            text-decoration: none;
            border-radius: 12px;
        }

        @media (max-width: 600px) {

            .caixa {
                padding: 25px 15px;
            }

            .estatisticas {
                grid-template-columns: 1fr;
            }

        }

    </style>

</head>

<body>

<div class="caixa">

    <h1>
        📊 Painel do AdivinheDev
    </h1>

    <p class="subtitulo">
        Estatísticas do seu jogo 🎮
    </p>

    <div class="estatisticas">

        <div class="card">

            <div class="icone">
                👥
            </div>

            <div class="numero">
                {{ visitas }}
            </div>

            <div class="nome">
                Visitantes únicos
            </div>

        </div>


        <div class="card online">

            <div class="icone">
                🟢
            </div>

            <div class="numero">
                {{ online }}
            </div>

            <div class="nome">
                Online agora*
            </div>

        </div>


        <div class="card">

            <div class="icone">
                🎮
            </div>

            <div class="numero">
                {{ partidas }}
            </div>

            <div class="nome">
                Partidas concluídas
            </div>

        </div>


        <div class="card">

            <div class="icone">
                🏆
            </div>

            <div class="numero">
                {{ vitorias }}
            </div>

            <div class="nome">
                Vitórias
            </div>

        </div>


        <div class="card">

            <div class="icone">
                💀
            </div>

            <div class="numero">
                {{ derrotas }}
            </div>

            <div class="nome">
                Derrotas
            </div>

        </div>


        <div class="card">

            <div class="icone">
                📈
            </div>

            <div class="numero">
                {{ taxa }}%
            </div>

            <div class="nome">
                Taxa de vitória
            </div>

        </div>

    </div>

    <p
        style="
            text-align:center;
            color:#777;
            font-size:13px;
            margin-top:20px;
        "
    >
        * Online = visitante que acessou o jogo
        nos últimos 60 segundos.
    </p>

    <a
        class="voltar"
        href="/"
    >
        🎮 Voltar para o jogo
    </a>

</div>

</body>

</html>
"""


# =========================================================
# ROTA ADMIN
# =========================================================

@app.route("/admin", methods=["GET", "POST"])
def admin():

    if not session.get("admin"):

        erro = False

        if request.method == "POST":

            senha = request.form.get(
                "senha",
                ""
            )

            if senha == ADMIN_SENHA:

                session["admin"] = True

                return redirect("/admin")

            erro = True

        return render_template_string(
            HTML_ADMIN_LOGIN,
            erro=erro
        )

    with conectar() as conexao:

        visitas = conexao.execute("""
            SELECT COUNT(*)
            FROM visitas
        """).fetchone()[0]

        online = conexao.execute("""
            SELECT COUNT(*)
            FROM visitas
            WHERE ultima_visita >=
            datetime('now', '-60 seconds')
        """).fetchone()[0]

        partidas = conexao.execute("""
            SELECT COUNT(*)
            FROM pontuacoes
        """).fetchone()[0]

        vitorias = conexao.execute("""
            SELECT COUNT(*)
            FROM pontuacoes
            WHERE resultado = 'Vitoria'
        """).fetchone()[0]

        derrotas = conexao.execute("""
            SELECT COUNT(*)
            FROM pontuacoes
            WHERE resultado = 'Derrota'
        """).fetchone()[0]

    if partidas > 0:

        taxa = round(
            (vitorias / partidas) * 100,
            1
        )

    else:

        taxa = 0

    return render_template_string(
        HTML_ADMIN,
        visitas=visitas,
        online=online,
        partidas=partidas,
        vitorias=vitorias,
        derrotas=derrotas,
        taxa=taxa
    )


# =========================================================
# INICIA BANCO
# =========================================================

criar_banco()


# =========================================================
# EXECUÇÃO LOCAL
# =========================================================

if __name__ == "__main__":
    app.run(debug=True)