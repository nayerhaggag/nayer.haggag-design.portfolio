document.addEventListener("DOMContentLoaded", function () {
  var galleryImages = document.querySelectorAll(".gallery img");
  if (!galleryImages.length) return;

  var overlay = document.createElement("div");
  overlay.className = "lightbox-overlay";

  var expandedImg = document.createElement("img");
  overlay.appendChild(expandedImg);
  document.body.appendChild(overlay);

  function openLightbox(src, alt) {
    expandedImg.src = src;
    expandedImg.alt = alt || "";
    overlay.classList.add("active");
    document.body.style.overflow = "hidden";
  }

  function closeLightbox() {
    overlay.classList.remove("active");
    document.body.style.overflow = "";
  }

  galleryImages.forEach(function (image) {
    image.addEventListener("click", function () {
      openLightbox(image.src, image.alt);
    });
  });

  overlay.addEventListener("click", closeLightbox);

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") closeLightbox();
  });
});
