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

/* RETAKE */

const retakeButton = document.getElementById("retake-button");

/* ERROR */

const uploadError = document.getElementById("upload-error");

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
   STOP CAMERA
========================= */

function stopCamera() {
  if (stream) {
    stream.getTracks().forEach((track) => track.stop());
    stream = null;
  }
}

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

  if (!file) return;

  const allowedTypes = ["image/jpeg", "image/jpg", "image/png"];

  if (!allowedTypes.includes(file.type)) {
    uploadError.textContent =
      "Unsupported file format. Please upload JPG, JPEG, or PNG.";

    this.value = "";
    return;
  }

  uploadError.textContent = "";

  const reader = new FileReader();

  reader.onload = function (e) {
    previewImage.src = e.target.result;
    previewImage.style.display = "block";

    camera.style.display = "none";
    captureButton.style.display = "none";

    stopCamera();

    uploadCard.classList.add("uploaded");

    /* FILE UPLOAD = NO RETAKE */

    analyzeButton.style.display = "inline-block";
    retakeButton.style.display = "none";
  };

  reader.readAsDataURL(file);
});

/* =========================
   OPEN CAMERA
========================= */

cameraButton.addEventListener("click", async () => {
  try {
    uploadError.textContent = "";

    stream = await navigator.mediaDevices.getUserMedia({
      video: true,
    });

    camera.srcObject = stream;

    camera.style.display = "block";

    previewImage.style.display = "none";

    captureButton.style.display = "inline-block";

    analyzeButton.style.display = "none";
    retakeButton.style.display = "none";

    /* HANYA TAKE SELFIE */

    selectButton.style.display = "none";
    cameraButton.style.display = "none";
  } catch (error) {
    console.error(error);
    alert("Unable to access camera.");
  }
});

/* =========================
   TAKE SELFIE
========================= */

captureButton.addEventListener("click", () => {
  const context = canvas.getContext("2d");

  canvas.width = camera.videoWidth;
  canvas.height = camera.videoHeight;

  context.drawImage(camera, 0, 0, canvas.width, canvas.height);

  previewImage.src = canvas.toDataURL("image/jpeg");
  previewImage.style.display = "block";

  camera.style.display = "none";
  captureButton.style.display = "none";

  stopCamera();

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

  uploadCard.classList.add("uploaded");

  analyzeButton.style.display = "inline-block";
  retakeButton.style.display = "inline-block";
});

/* =========================
   RETAKE PHOTO
========================= */

retakeButton.addEventListener("click", async () => {
  try {
    stream = await navigator.mediaDevices.getUserMedia({
      video: true,
    });

    camera.srcObject = stream;

    camera.style.display = "block";

    previewImage.style.display = "none";

    captureButton.style.display = "inline-block";

    analyzeButton.style.display = "none";
    retakeButton.style.display = "none";

    uploadCard.classList.remove("uploaded");

    imageInput.value = "";
  } catch (error) {
    console.error(error);
    alert("Unable to access camera.");
  }
});

/* =========================
   ANALYZE LOADING
========================= */

form.addEventListener("submit", function (e) {
  if (!imageInput.files.length) {
    e.preventDefault();

    uploadError.textContent = "Please upload or capture a photo first.";

    return;
  }

  e.preventDefault();

  analyzeButton.style.display = "none";
  retakeButton.style.display = "none";
  captureButton.style.display = "none";
  camera.style.display = "none";

  uploadCard.classList.add("loading");

  loadingBar.style.width = "0%";

  setTimeout(() => {
    loadingBar.style.width = "100%";
  }, 50);

  setTimeout(() => {
    form.submit();
  }, 3000);
});

/* =========================
   CLEANUP
========================= */

window.addEventListener("beforeunload", () => {
  stopCamera();
});
