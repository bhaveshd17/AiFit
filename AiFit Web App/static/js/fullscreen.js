let fullscreen = document.getElementById("fullscreen_image");

fullscreen.addEventListener("click", () => {
  if (!document.fullscreenElement) {
    fullscreen?.requestFullscreen();
  } else {
    document.exitFullscreen();
  }
});