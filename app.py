from flask import Flask, request, render_template_string, session
import random
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = "adivinhedev-chave-secreta"

BANCO = Path(__file__).with_name("ranking.db")


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


HTML = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AdivinheDev</title>

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            min-height: 100vh;
            padding: 25px 12px;
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #111827, #2563eb);
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .caixa {
            width: 100%;
            max-width: 950px;
            background: white;
            border-radius: 25px;
            padding: 40px;
            text-align: center;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.35);
        }

        h1 {
            font-size: 48px;
            margin: 0 0 20px;
        }

        h2 {
            font-size: 28px;
        }

        p {
            font-size: 20px;
        }

        input {
            width: 90%;
            max-width: 500px;
            padding: 16px;
            margin: 10px;
            font-size: 20px;
            text-align: center;
            border: 2px solid #aaa;
            border-radius: 12px;
        }

        input:focus {
            outline: 2px solid #2563eb;
        }

        button {
            padding: 15px 25px;
            margin: 10px 5px;
            font-size: 19px;
            border: none;
            border-radius: 12px;
            background: #2563eb;
            color: white;
            cursor: pointer;
        }

        button:hover {
            background: #1d4ed8;
        }

        .tentativas {
            font-size: 23px;
            margin: 20px;
        }

        .mensagem {
            font-size: 25px;
            font-weight: bold;
            margin: 20px;
        }

        .eficiencia {
            font-size: 30px;
            font-weight: bold;
            margin: 20px;
            color: #2563eb;
        }

        .painel {
            margin-top: 35px;
            padding: 25px;
            background: #f3f4f6;
            border-radius: 18px;
            text-align: left;
        }

        .painel h2 {
            text-align: center;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }

        th, td {
            padding: 12px 8px;
            border-bottom: 1px solid #d1d5db;
            text-align: center;
            font-size: 16px;
        }

        th {
            background: #e5e7eb;
        }

        .vazio {
            text-align: center;
            color: #555;
        }

        .colunas {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }

        .pequeno {
            font-size: 14px;
            color: #555;
        }

        @media (max-width: 650px) {
            .caixa {
                padding: 25px 12px;
            }

            h1 {
                font-size: 36px;
            }

            .colunas {
                grid-template-columns: 1fr;
            }

            th, td {
                padding: 9px 4px;
                font-size: 14px;
            }
        }
    </style>
</head>

<body>

<div class="caixa">

    <h1>🎮 AdivinheDev</h1>

    {% if not iniciado %}

        <h2>Vamos começar!</h2>
        <p>Digite seu nome para começar uma nova partida.</p>

        <form method="POST">
            <input
                type="text"
                name="nome"
                placeholder="Seu nome"
                maxlength="30"
                required
                autofocus
            >
            <br>
            <button type="submit">Começar jogo 🚀</button>
        </form>

    {% else %}

        <h2>Boa sorte, {{ nome }}! 🦫</h2>

        <p>
            Estou pensando em um número entre
            <strong>1 e 100</strong>.
        </p>

        <div class="tentativas">
            ❤️ Tentativas: <strong>{{ tentativas }}/10</strong>
        </div>

        {% if not finalizado %}

            <form method="POST">
                <input
                    id="palpite"
                    type="number"
                    name="palpite"
                    min="1"
                    max="100"
                    placeholder="Digite seu palpite"
                    required
                    autofocus
                >
                <br>
                <button type="submit">Adivinhar! 🎯</button>
            </form>

        {% endif %}

        {% if mensagem %}
            <div class="mensagem">{{ mensagem }}</div>
        {% endif %}

        {% if finalizado %}

            <div class="eficiencia">
                📊 Eficiência: {{ eficiencia }}%
            </div>

            <p>
                Sua pontuação nesta partida:
                <strong>{{ eficiencia }} pontos</strong>
            </p>

            <form method="POST">
                <button type="submit" name="novo_jogo" value="1">
                    🔄 Jogar novamente
                </button>
            </form>

        {% endif %}

    {% endif %}

    <div class="colunas">

        <div class="painel">
            <h2>🏆 Ranking geral</h2>

            <p class="pequeno">
                Melhores pontuações de cada jogador.
            </p>

            <table>
                <tr>
                    <th>#</th>
                    <th>Jogador</th>
                    <th>Recorde</th>
                </tr>

                {% for jogador in ranking %}
                    <tr>
                        <td>
                            {% if loop.index == 1 %}
                                🥇
                            {% elif loop.index == 2 %}
                                🥈
                            {% elif loop.index == 3 %}
                                🥉
                            {% else %}
                                {{ loop.index }}
                            {% endif %}
                        </td>
                        <td>{{ jogador["nome"] }}</td>
                        <td>{{ jogador["melhor"] }}%</td>
                    </tr>
                {% else %}
                    <tr>
                        <td colspan="3" class="vazio">
                            Ainda não há pontuações.
                        </td>
                    </tr>
                {% endfor %}
            </table>
        </div>

        <div class="painel">
            <h2>📜 Minhas partidas</h2>

            {% if iniciado %}
                <p class="pequeno">
                    Histórico de {{ nome }}.
                </p>

                <table>
                    <tr>
                        <th>Resultado</th>
                        <th>Pontos</th>
                        <th>Tentativas</th>
                    </tr>

                    {% for partida in historico %}
                        <tr>
                            <td>{{ partida["resultado"] }}</td>
                            <td>{{ partida["pontuacao"] }}%</td>
                            <td>{{ partida["tentativas"] }}/10</td>
                        </tr>
                    {% else %}
                        <tr>
                            <td colspan="3" class="vazio">
                                Jogue para registrar sua primeira partida!
                            </td>
                        </tr>
                    {% endfor %}
                </table>
            {% else %}
                <p class="vazio">
                    Digite seu nome para ver seu histórico.
                </p>
            {% endif %}
        </div>

    </div>

</div>

<script>
    window.onload = function() {
        const campo = document.getElementById("palpite");

        if (campo) {
            campo.focus();
        }
    };

    function tocarSom(tipo) {
        const audio = new AudioContext();
        const oscilador = audio.createOscillator();
        const ganho = audio.createGain();

        oscilador.connect(ganho);
        ganho.connect(audio.destination);

        if (tipo === "erro") {
            oscilador.type = "sawtooth";
            oscilador.frequency.value = 180;
            ganho.gain.value = 0.2;
            oscilador.start();
            oscilador.stop(audio.currentTime + 0.25);
        } else {
            oscilador.type = "sine";
            oscilador.frequency.setValueAtTime(523, audio.currentTime);
            oscilador.frequency.setValueAtTime(659, audio.currentTime + 0.15);
            oscilador.frequency.setValueAtTime(784, audio.currentTime + 0.30);
            ganho.gain.value = 0.2;
            oscilador.start();
            oscilador.stop(audio.currentTime + 0.55);
        }
    }

    const resultado = "{{ resultado }}";

    if (resultado === "erro") {
        tocarSom("erro");
    }

    if (resultado === "acerto") {
        tocarSom("acerto");
    }
</script>

</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def inicio():

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

        if (
            "nome" in session
            and not session.get("finalizado", False)
        ):
            try:
                palpite = int(request.form["palpite"])
            except (ValueError, TypeError):
                palpite = 0

            if palpite < 1 or palpite > 100:

                session["mensagem"] = (
                    "⚠️ Digite um número entre 1 e 100!"
                )
                session["resultado"] = ""

            else:
                palpites = session.get("palpites", [])

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
                            f"🎉 PARABÉNS, {session['nome']}! "
                            "Você acertou o número!"
                        )
                        session["finalizado"] = True
                        session["resultado"] = "acerto"

                    elif palpite < numero:

                        session["mensagem"] = "📈 O número é MAIOR!"
                        session["resultado"] = "erro"

                    else:

                        session["mensagem"] = "📉 O número é MENOR!"
                        session["resultado"] = "erro"

                    if tentativas >= 10 and palpite != numero:

                        session["mensagem"] = (
                            f"💀 Fim de jogo! O número era {numero}."
                        )
                        session["eficiencia"] = 0
                        session["finalizado"] = True

                    if (
                        session["finalizado"]
                        and not session.get("salvo", False)
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
        buscar_historico(session["nome"])
        if iniciado else []
    )

    return render_template_string(
        HTML,
        iniciado=iniciado,
        nome=session.get("nome", ""),
        tentativas=session.get("tentativas", 0),
        mensagem=session.get("mensagem", ""),
        finalizado=session.get("finalizado", False),
        eficiencia=session.get("eficiencia", 0),
        resultado=session.get("resultado", ""),
        ranking=ranking,
        historico=historico
    )


criar_banco()

if __name__ == "__main__":
    app.run(debug=True)