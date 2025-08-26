// Dark/Light Theme Toggle
const themeToggle = document.getElementById("themeToggle");
const themeIcon = document.getElementById("themeIcon");
themeToggle.addEventListener("click", () => {
  document.body.classList.toggle("dark");
  themeIcon.textContent = document.body.classList.contains("dark") ? "☀️" : "🌙";
});

// Guess Logic
async function makeGuess() {
  const guessInput = document.getElementById("guessInput");
  const alertBox = document.getElementById("alertBox");
  const playAgainBtn = document.getElementById("playAgain");
  const newHighScore = document.getElementById("newHighScore");

  let guess = guessInput.value;
  if (!guess) return;

  const response = await fetch("/guess", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({guess})
  });
  const data = await response.json();

  alertBox.classList.remove("d-none", "alert-success", "alert-danger", "alert-warning");
  alertBox.classList.add(
    data.status === "won" ? "alert-success" :
    data.status === "lost" ? "alert-danger" : "alert-warning"
  );
  alertBox.textContent = data.message;

  // Game Won
  if (data.status === "won") {
    playAgainBtn.style.display = "inline-block";
    if (data.message.includes("New best score")) {
      newHighScore.style.display = "block";
    }
  }
  // Game Lost
  if (data.status === "lost") {
    playAgainBtn.style.display = "inline-block";
  }

  guessInput.value = "";
}

// Reset Game
async function playAgain() {
  await fetch("/reset", {method: "POST"});
  window.location.reload();
}
