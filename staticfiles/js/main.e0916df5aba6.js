document.addEventListener("DOMContentLoaded", function () {
  feed = document.getElementById("cards-list");
  if (feed) {
    localStorage.setItem("originUrl", window.location.href);
  }
});

document.addEventListener("DOMContentLoaded", function () {
  var originUrl = localStorage.getItem("originUrl");

  var backButton = document.getElementById("back-button");
  if (backButton) {
    backButton.href = originUrl;
  }
});
