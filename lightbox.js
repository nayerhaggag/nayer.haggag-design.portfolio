document.addEventListener("DOMContentLoaded", function () {
  var galleryImages = document.querySelectorAll(".gallery img");
  if (!galleryImages.length) return;

  var images = Array.prototype.slice.call(galleryImages);
  var currentIndex = 0;

  var overlay = document.createElement("div");
  overlay.className = "lightbox-overlay";

  var expandedImg = document.createElement("img");
  overlay.appendChild(expandedImg);

  var prevBtn = document.createElement("button");
  prevBtn.className = "lightbox-nav lightbox-prev";
  prevBtn.setAttribute("aria-label", "Previous image");
  prevBtn.innerHTML = "&#8249;";
  overlay.appendChild(prevBtn);

  var nextBtn = document.createElement("button");
  nextBtn.className = "lightbox-nav lightbox-next";
  nextBtn.setAttribute("aria-label", "Next image");
  nextBtn.innerHTML = "&#8250;";
  overlay.appendChild(nextBtn);

  document.body.appendChild(overlay);

  function showImage(index) {
    currentIndex = (index + images.length) % images.length;
    var image = images[currentIndex];
    expandedImg.src = image.src;
    expandedImg.alt = image.alt || "";
  }

  function openLightbox(index) {
    showImage(index);
    overlay.classList.add("active");
    document.body.style.overflow = "hidden";
  }

  function closeLightbox() {
    overlay.classList.remove("active");
    document.body.style.overflow = "";
  }

  function showPrev() {
    showImage(currentIndex - 1);
  }

  function showNext() {
    showImage(currentIndex + 1);
  }

  images.forEach(function (image, index) {
    image.addEventListener("click", function () {
      openLightbox(index);
    });
  });

  overlay.addEventListener("click", function (event) {
    if (event.target === overlay) closeLightbox();
  });

  expandedImg.addEventListener("click", closeLightbox);

  prevBtn.addEventListener("click", function (event) {
    event.stopPropagation();
    showPrev();
  });

  nextBtn.addEventListener("click", function (event) {
    event.stopPropagation();
    showNext();
  });

  document.addEventListener("keydown", function (event) {
    if (!overlay.classList.contains("active")) return;
    if (event.key === "Escape") closeLightbox();
    if (event.key === "ArrowLeft") showPrev();
    if (event.key === "ArrowRight") showNext();
  });
});
