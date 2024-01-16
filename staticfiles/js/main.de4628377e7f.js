document.addEventListener("DOMContentLoaded", function () {
  movieFeed = document.getElementById("movie-feed");
  if (movieFeed) {
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
