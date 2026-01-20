from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "SUA_CHAVE_SECRETA_AQUI"  # troca por algo seguro
app.permanent_session_lifetime = timedelta(hours=24)  # duração da sessão

# 🔐 Password única (tu decides)
BOT_PASSWORD = "meuSuperPIN123"

# Histórico global (simples e funcional)
historico = []
MAX_RODADAS = 3

# Banca inicial
bank_balance = 50000  # AOA
recommended_percent = 5  # %
stop_loss_percent = -10  # %
daily_goal_percent = 15  # %

# ---------- FUNÇÕES ----------

def verificar_sinal(hist):
    """
    Regra EXATA após 3 resultados:
    - BBB → sinal BANKER + EMPATE
    - PPP → sinal PLAYER + EMPATE
    Caso contrário: sem sinal
    """
    if len(hist) < 3:
        return None

    ultimos = hist[-3:]

    if ultimos == ["B", "B", "B"]:
        return "🚨 SINAL CONFIRMADO: APOSTAR BANKER + EMPATE"
    if ultimos == ["P", "P", "P"]:
        return "🚨 SINAL CONFIRMADO: APOSTAR PLAYER + EMPATE"

    return None

# ---------- ROTAS ----------

# Login
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        senha = request.form.get("password")
        if senha == BOT_PASSWORD:
            session.permanent = True
            session["logged_in"] = True
            return redirect(url_for("bot"))
        else:
            return render_template("login.html", error="Senha incorreta!")
    return render_template("login.html")

# Bot principal
@app.route("/bot")
def bot():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("index.html", historico=historico,
                           bank_balance=bank_balance,
                           recommended_percent=recommended_percent,
                           stop_loss=stop_loss_percent,
                           daily_goal=daily_goal_percent)

# Logout opcional
@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("login"))

# Adicionar resultado (API para JS)
@app.route("/add", methods=["POST"])
def add_resultado():
    global historico

    dado = request.json.get("resultado", "").upper()

    if dado not in ["P", "B", "T"]:
        return jsonify({"erro": "Entrada inválida"}), 400

    historico.append(dado)
    sinal = verificar_sinal(historico)

    return jsonify({
        "historico": historico,
        "sinal": sinal
    })

# Resetar histórico
@app.route("/reset", methods=["POST"])
def reset():
    global historico
    historico = []
    return jsonify({"status": "resetado"})

# 🔥 MUITO IMPORTANTE PARA FUNCIONAR EM QUALQUER DISPOSITIVO
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
