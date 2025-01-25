let selectedElement = null;

document.querySelectorAll("svg *[id]").forEach((element) => {
  element.addEventListener("click", function () {
    selectedElement = this;
    this.style.stroke = "#000";
    this.style.strokeWidth = "2";
  });
});

function applyColor() {
  if (selectedElement) {
    const color = document.getElementById("color-picker").value;
    selectedElement.setAttribute("fill", color);
    selectedElement.style.stroke = "none";
    selectedElement = null;
  }
}

document.getElementById("close").addEventListener("click", () => {
  window.location.href = "/";
});
