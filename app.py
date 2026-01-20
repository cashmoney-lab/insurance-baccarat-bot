from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Histórico global (simples e funcional)
historico = []
MAX_RODADAS = 3


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


@app.route("/")
def index():
    return render_template("index.html", historico=historico)


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


@app.route("/reset", methods=["POST"])
def reset():
    global historico
    historico = []
    return jsonify({"status": "resetado"})


# 🔥 MUITO IMPORTANTE PARA FUNCIONAR EM QUALQUER DISPOSITIVO
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
