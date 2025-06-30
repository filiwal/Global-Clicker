let counter = 0;
const input = document.getElementById("input");
const inc = document.getElementById("increment");
const dec = document.getElementById("decrement");

let money = 0;
const moneyInput = document.getElementById("money"); // <-- match HTML

function play() {
  var audio = new Audio('news-ting-6832.mp3');
  audio.play();
}

function play2() {
  var audio2 = new Audio('fail-144746.mp3');
  audio2.play();
}

// Connect to FastAPI WebSocket
const ws = new WebSocket("ws://localhost:8000/ws");

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (typeof data.counter !== "undefined") {
    counter = data.counter;
    if (input) input.value = counter;
  }
  if (typeof data.money !== "undefined" && moneyInput) {
    money = data.money;
    moneyInput.value = money;
  }
};

if (inc) {
  inc.onclick = () => {
    play();
    ws.send(JSON.stringify({ action: "increment" }));
    ws.send(JSON.stringify({ action: "increment-money" }));
  };
}

if (dec) {
  dec.onclick = () => {
    play2();
    ws.send(JSON.stringify({ action: "decrement" }));
    ws.send(JSON.stringify({ action: "increment-money" }));
  };
}