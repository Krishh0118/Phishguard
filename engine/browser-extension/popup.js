fetch("http://127.0.0.1:8501/api/check-url", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ url: url })
})
.then(res => res.json())
.then(data => {
  document.getElementById("result").innerText =
    data.label + " (Score: " + data.score + ")";
})
.catch(() => {
  document.getElementById("result").innerText = "API not reachable";
});
