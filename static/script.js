const passwordInput = document.getElementById("password");
const toggleBtn = document.getElementById("toggle");
const meterFill = document.getElementById("meter-fill");
const ratingText = document.getElementById("rating");
const feedbackList = document.getElementById("feedback");
const breachBtn = document.getElementById("breach-btn");
const breachResult = document.getElementById("breach-result");

const COLORS = { Weak: "#ef4444", Medium: "#f59e0b", Strong: "#16a34a" };

// Show / hide the password
toggleBtn.addEventListener("click", () => {
  const hidden = passwordInput.type === "password";
  passwordInput.type = hidden ? "text" : "password";
  toggleBtn.textContent = hidden ? "Hide" : "Show";
});

// Live strength check while typing
passwordInput.addEventListener("input", async () => {
  breachResult.textContent = "";
  const password = passwordInput.value;

  if (password === "") {
    meterFill.style.width = "0";
    ratingText.textContent = "Start typing to see the strength.";
    feedbackList.innerHTML = "";
    return;
  }

  const response = await fetch("/api/strength", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ password })
  });
  const data = await response.json();

  meterFill.style.width = (data.score / data.max_score) * 100 + "%";
  meterFill.style.background = COLORS[data.rating];
  ratingText.textContent = `${data.rating} (${data.score}/${data.max_score})`;
  feedbackList.innerHTML = data.feedback.map(tip => `<li>${tip}</li>`).join("");
});

// Breach check on button click
breachBtn.addEventListener("click", async () => {
  const password = passwordInput.value;
  breachResult.className = "breach-result";

  if (password === "") {
    breachResult.textContent = "Please type a password first.";
    return;
  }

  breachResult.textContent = "Checking...";
  const response = await fetch("/api/breach", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ password })
  });
  const data = await response.json();

  if (!response.ok) {
    breachResult.textContent = data.error;
  } else if (data.breached) {
    breachResult.textContent = `Found in ${data.count.toLocaleString()} known breaches. Do not use it.`;
    breachResult.classList.add("bad");
  } else {
    breachResult.textContent = "Not found in known breaches.";
    breachResult.classList.add("good");
  }
});
