let history = [];

function addResult(r) {
    history.push(r);

    const list = document.getElementById("historyList");
    const item = document.createElement("li");
    item.textContent = new Date().toLocaleTimeString() + " → " + r;
    list.prepend(item);

    if (history.length >= 3) {
        analyze();
    }
}

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
