/* =========================
   ELEMENTS
========================= */

const uploadCard = document.querySelector(".upload-card");

const form = document.querySelector(".upload-card form");

/* FILE */

const imageInput = document.getElementById("image-input");

const selectButton = document.getElementById("select-button");

/* PREVIEW */

const previewImage = document.getElementById("preview-image");

/* ANALYZE */

const analyzeButton = document.getElementById("analyze-button");

/* LOADING */

const loadingBar = document.querySelector(".loading-bar");

/* CAMERA */

const cameraButton = document.getElementById("camera-button");

const captureButton = document.getElementById("capture-button");

const camera = document.getElementById("camera");

const canvas = document.getElementById("camera-canvas");

/* STREAM */

let stream;

/* =========================
   SELECT FILE
========================= */

selectButton.addEventListener("click", () => {
  imageInput.click();
});

/* =========================
   FILE UPLOAD
========================= */

imageInput.addEventListener("change", function () {
  const file = this.files[0];

  if (file && file.type.startsWith("image/")) {
    const reader = new FileReader();

    reader.onload = function (e) {
      /* SHOW PREVIEW */

      previewImage.src = e.target.result;

      previewImage.style.display = "block";

      /* HIDE CAMERA */

      camera.style.display = "none";

      /* HIDE TAKE SELFIE */

      captureButton.style.display = "none";

      /* STOP CAMERA */

      if (stream) {
        stream.getTracks().forEach((track) => track.stop());
      }

      /* UPLOADED STATE */

      uploadCard.classList.add("uploaded");

      /* SHOW ANALYZE */

      analyzeButton.style.display = "inline-block";
    };

    reader.readAsDataURL(file);
  }
});

/* =========================
   OPEN CAMERA
========================= */

cameraButton.addEventListener("click", async () => {
  try {
    stream = await navigator.mediaDevices.getUserMedia({
      video: true,
    });

    /* SHOW CAMERA */

    camera.srcObject = stream;

    camera.style.display = "block";

    /* SHOW TAKE SELFIE */

    captureButton.style.display = "inline-block";

    /* HIDE PREVIEW */

    previewImage.style.display = "none";
  } catch (error) {
    alert("Unable to access camera.");

    console.error(error);
  }
});

/* =========================
   TAKE SELFIE
========================= */

captureButton.addEventListener("click", () => {
  const context = canvas.getContext("2d");

  /* CANVAS SIZE */

  canvas.width = camera.videoWidth;

  canvas.height = camera.videoHeight;

  /* DRAW FRAME */

  context.drawImage(camera, 0, 0, canvas.width, canvas.height);

  /* SHOW PREVIEW */

  previewImage.src = canvas.toDataURL("image/jpeg");

  previewImage.style.display = "block";

  /* HIDE CAMERA */

  camera.style.display = "none";

  /* HIDE TAKE SELFIE BUTTON */

  captureButton.style.display = "none";

  /* STOP CAMERA */

  if (stream) {
    stream.getTracks().forEach((track) => track.stop());
  }

  /* CONVERT SELFIE TO FILE */

  canvas.toBlob(
    (blob) => {
      const file = new File([blob], "selfie.jpg", {
        type: "image/jpeg",
      });

      const dataTransfer = new DataTransfer();

      dataTransfer.items.add(file);

      imageInput.files = dataTransfer.files;
    },
    "image/jpeg",
    0.9,
  );

  /* UPLOADED STATE */

  uploadCard.classList.add("uploaded");

  /* SHOW ANALYZE */

  analyzeButton.style.display = "inline-block";
});

/* =========================
   ANALYZE LOADING
========================= */

form.addEventListener("submit", function (e) {
  e.preventDefault();

  /* HIDE ANALYZE */

  analyzeButton.style.display = "none";

  /* HIDE TAKE SELFIE */

  captureButton.style.display = "none";

  /* HIDE CAMERA */

  camera.style.display = "none";

  /* SHOW LOADING */

  uploadCard.classList.add("loading");

  /* RESET */

  loadingBar.style.width = "0%";

  /* START */

  setTimeout(() => {
    loadingBar.style.width = "100%";
  }, 50);

  /* SUBMIT */

  setTimeout(() => {
    form.submit();
  }, 3000);
});