const inputText = document.getElementById("inputText");
const outputText = document.getElementById("outputText");
const cleanButton = document.getElementById("cleanButton");
const clearButton = document.getElementById("clearButton");
const clearOutputButton = document.getElementById("clearOutputButton");
const copyButton = document.getElementById("copyButton");
const downloadButton = document.getElementById("downloadButton");
const inputStats = document.getElementById("inputStats");
const outputStats = document.getElementById("outputStats");
const outputStatus = document.getElementById("outputStatus");
const toast = document.getElementById("toast");

function showToast(message) {
  toast.textContent = message;
  toast.classList.add("show");
  window.clearTimeout(showToast.timer);
  showToast.timer = window.setTimeout(() => toast.classList.remove("show"), 2300);
}

function updateInputStats() {
  const count = inputText.value.length;
  inputStats.textContent = `${count.toLocaleString()} character${count === 1 ? "" : "s"}`;
}
inputText.addEventListener("input", updateInputStats);

cleanButton.addEventListener("click", async () => {
  if (!inputText.value.trim()) {
    showToast("Paste some data to get started.");
    inputText.focus();
    return;
  }

  cleanButton.disabled = true;
  cleanButton.querySelector("span:first-child").textContent = "Processing...";
  try {
    const response = await fetch("/api/tools/phone-cleanser", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: inputText.value })
    });
    if (!response.ok) throw new Error("The server could not process this request.");
    const data = await response.json();
    outputText.value = data.result || "";
    outputStats.textContent = `${data.processed_rows} row${data.processed_rows === 1 ? "" : "s"}`;
    outputStatus.textContent = data.processed_rows ? "CLEANING COMPLETE" : "NO MATCHING ROWS";
    copyButton.disabled = !data.result;
    downloadButton.disabled = !data.result;
    clearOutputButton.disabled = !data.result;
    showToast(data.processed_rows ? `${data.processed_rows} row(s) cleaned successfully.` : "No rows with detectable numbers were found.");
  } catch (error) {
    showToast(error.message || "Something went wrong.");
  } finally {
    cleanButton.disabled = false;
    cleanButton.querySelector("span:first-child").textContent = "Clean data";
  }
});

clearButton.addEventListener("click", () => {
  inputText.value = "";
  updateInputStats();
  inputText.focus();
});

clearOutputButton.addEventListener("click", () => {
  outputText.value = "";
  outputStats.textContent = "0 rows";
  outputStatus.textContent = "READY WHEN YOU ARE";
  copyButton.disabled = true;
  downloadButton.disabled = true;
  clearOutputButton.disabled = true;
  showToast("Output cleared.");
});

copyButton.addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(outputText.value);
    showToast("Output copied to clipboard.");
  } catch {
    outputText.select();
    document.execCommand("copy");
    showToast("Output copied to clipboard.");
  }
});

downloadButton.addEventListener("click", () => {
  const blob = new Blob([outputText.value], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "kanekes-cleaned-phone-numbers.txt";
  link.click();
  URL.revokeObjectURL(url);
});

document.getElementById("mobileMenu").addEventListener("click", () => {
  document.getElementById("sidebar").classList.toggle("open");
});

updateInputStats();
