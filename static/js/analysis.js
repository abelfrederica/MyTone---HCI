/* =========================
   ELEMENTS
========================= */

const uploadCard = document.querySelector(".upload-card");

const selectButton = document.getElementById("select-button");

const imageInput = document.getElementById("image-input");

const previewImage = document.getElementById("preview-image");

const analyzeButton = document.getElementById("analyze-button");

const loadingBar = document.querySelector(".loading-bar");

const form = document.querySelector(".upload-card form");

/* =========================
   SELECT FILE
========================= */

selectButton.addEventListener("click", () => {
  imageInput.click();
});

/* =========================
   IMAGE UPLOAD
========================= */

imageInput.addEventListener("change", function () {
  const file = this.files[0];

  if (file && file.type.startsWith("image/")) {
    /* PREVIEW IMAGE */

    const reader = new FileReader();

    reader.onload = function (e) {
      previewImage.src = e.target.result;

      previewImage.style.display = "block";
    };

    reader.readAsDataURL(file);

    /* SHOW UPLOADED STATE */

    uploadCard.classList.add("uploaded");

    /* SHOW BUTTON */

    analyzeButton.style.display = "inline-block";
  }
});

/* =========================
   ANALYZE LOADING
========================= */

form.addEventListener("submit", function (e) {
  e.preventDefault();

  /* HIDE BUTTON */

  analyzeButton.style.display = "none";

  /* START LOADING */

  loadingBar.style.width = "100%";

  /* GO TO RESULT PAGE */

  setTimeout(() => {
    form.submit();
  }, 3000);
});
