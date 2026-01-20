// HISTÓRICO SIMPLES
let history = [];

// HISTÓRICO AVANÇADO
let historyAdvancedData = [];

// BANCA
let bankBalance = 50000; // saldo inicial AOA
const recommendedPercent = 5; // % recomendado por aposta
const stopLossPercent = -10; // % diário
const dailyGoalPercent = 15; // % diário

// ADICIONAR RESULTADO
function addResult(r) {
    // HISTÓRICO SIMPLES
    history.push(r);
    const list = document.getElementById("historyList");
    const item = document.createElement("li");
    item.textContent = new Date().toLocaleTimeString() + " → " + r;
    list.prepend(item);

    // HISTÓRICO AVANÇADO
    const now = new Date();
    const timeStr = now.toLocaleTimeString();

    historyAdvancedData.push({
        time: timeStr,
        result: r,
        signal: getSignal(r)
    });

    updateHistoryTable();
    updateBankDisplay();

    // ANALISE SE TIVER 3 RESULTADOS
    if (history.length >= 3) {
        analyze();
    }
}

// RETORNA O SINAL PARA O RESULTADO
function getSignal(result) {
    if (result === "B") return "🟢 APOSTAR BANKER";
    if (result === "P") return "🟢 APOSTAR PLAYER";
    if (result === "T") return "🛡️ EMPATE";
    return "";
}

// ATUALIZA TABELA DO HISTÓRICO AVANÇADO
function updateHistoryTable() {
    const tbody = document.getElementById("historyAdvanced");
    tbody.innerHTML = ""; // limpa tabela
    historyAdvancedData.slice(-10).forEach(item => { // últimos 10
        const tr = document.createElement("tr");
        tr.innerHTML = `<td>${item.time}</td><td>${item.result}</td><td>${item.signal}</td>`;
        tbody.appendChild(tr);
    });
}

// ATUALIZA EXIBIÇÃO DE BANCA
function updateBankDisplay() {
    document.getElementById("bankBalance").textContent = bankBalance.toLocaleString();
    document.getElementById("recommendPercent").textContent = recommendedPercent + "%";
    document.getElementById("stopLoss").textContent = stopLossPercent + "%";
    document.getElementById("dailyGoal").textContent = dailyGoalPercent + "%";
}

// FUNÇÃO DE ANÁLISE (mantida da FASE 1)
function analyze() {
    const last = history.slice(-3).join("");
    const status = document.getElementById("status");
    const signal = document.getElementById("signal");

    if (last === "BBB") {
        status.className = "status win";
        status.innerHTML = "😄🔥 ENTRAR AGORA";
        signal.innerHTML = "🟢 APOSTAR BANKER <br> 🛡️ EMPATE";
    } 
    else if (last === "PPP") {
        status.className = "status win";
        status.innerHTML = "😄🔥 ENTRAR AGORA";
        signal.innerHTML = "🟢 APOSTAR PLAYER <br> 🛡️ EMPATE";
    } 
    else {
        status.className = "status wait";
        status.innerHTML = "😞⛔ AGUARDAR";
        signal.innerHTML = "";
    }
}
