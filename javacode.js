let counter = 0;
const input = document.getElementById("input");
const inc = document.getElementById("increment");
const dec = document.getElementById("decrement");

function play() {
  var audio = new Audio('news-ting-6832.mp3');
  audio.play();
}

function play2() {
  var audio2 = new Audio('fail-144746.mp3');
  audio2.play();
}

//Connect to FastAPI WebSocket
const ws = new WebSocket("ws://localhost:8000/ws");

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  counter = data.counter;
  input.value = counter;
};

inc.onclick = () => {
  play();
  input.value = ++counter;
  ws.send(JSON.stringify({ action: "increment" }));
};

dec.onclick = () => {
  play2();
  input.value = --counter;
  ws.send(JSON.stringify({ action: "decrement" }));
};
