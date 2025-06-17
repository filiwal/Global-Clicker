var counter = 0;
 
function play() {
  var audio = new Audio('news-ting-6832.mp3');
  audio.play();
}

function play2() {
  var audio2 = new Audio('fail-144746.mp3');
  audio2.play();
}

function increment() {
  counter++;
}
 
function decrement() {
  counter--;
}
 
function get() {
  return counter;
}
 
const inc = document.getElementById("increment");
const input = document.getElementById("input");
const dec = document.getElementById("decrement");
 
inc.addEventListener("click", () => {
  increment();
  input.value = get();
});
 
dec.addEventListener("click", () => {
  if (input.value > 0) {
    decrement();
  }
  input.value = get();
});