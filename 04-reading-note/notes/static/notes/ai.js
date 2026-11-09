// AI 버튼을 누르면 버튼을 잠그고 기다림 안내를 보여 준다(여러 번 눌러도 한 번만 보낸다).
document.querySelectorAll("form.ai-form").forEach(function (form) {
  form.addEventListener("submit", function () {
    var button = form.querySelector("button");
    button.disabled = true;
    button.setAttribute("aria-busy", "true");
    button.textContent = form.dataset.waiting || "AI가 일하는 중입니다. 30초쯤 걸릴 수 있습니다.";
  });
});
