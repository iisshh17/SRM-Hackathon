let selectedPart = null;

document.querySelectorAll("svg rect, svg path, svg circle").forEach((part) => {
  part.addEventListener("click", (e) => {
    selectedPart = e.target;
    alert(`You selected the ${selectedPart.id}`);
  });
});


function applyColor() {
  const color = document.getElementById("color-picker").value;
  if (selectedPart) {
    selectedPart.setAttribute("fill", color);
  } else {
    alert("Please select a part to color.");
  }
}

const closeBtn = document.getElementById("close")
closeBtn.addEventListener("click",()=>{
  window.location.href="/";
})