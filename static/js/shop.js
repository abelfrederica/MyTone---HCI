const slides = document.querySelectorAll(".shop-slide");
const nextBtn = document.querySelector(".next-btn");
const prevBtn = document.querySelector(".prev-btn");

const sectionTitle = document.getElementById("shop-section-title");
const sectionDescription = document.getElementById("shop-section-description");

const productGrid = document.getElementById("product-grid");
const exploreBtn = document.querySelector(".shop-score");

let currentSlide = 0;
let expanded = false;

/* =========================
   RENDER SHOP CONTENT
========================= */

function updateShopContent(index) {
  if (!shopData || !shopData[index]) return;

  const data = shopData[index];

  sectionTitle.textContent = data.section_title;
  sectionDescription.textContent = data.section_description;

  productGrid.innerHTML = "";

  const limit = expanded ? 16 : 4;

  data.products.slice(0, limit).forEach((product) => {
    productGrid.innerHTML += `
      <div class="product-card">
        <div class="product-image">
          <span class="product-tag">SHOPEE</span>
          <img src="/static/${product.image}" alt="${product.name}">
        </div>

        <div class="product-info">
          <div class="product-top">
            <h3>${product.name}</h3>
            <span class="product-price">${product.price}</span>
          </div>

          <span class="product-color">COLOR: ${product.color}</span>

          <button class="product-button" data-link="${product.link}">
            BUY ON SHOPEE
          </button>
        </div>
      </div>
    `;
  });
}

/* =========================
   EVENT DELEGATION (IMPORTANT)
========================= */

productGrid.addEventListener("click", (e) => {
  const btn = e.target.closest(".product-button");
  if (!btn) return;

  const link = btn.dataset.link;
  if (link) {
    window.open(link, "_blank");
  }
});

/* =========================
   SHOW SLIDE
========================= */

function showSlide(index) {
  slides.forEach((s) => s.classList.remove("active"));

  if (!slides[index]) return;

  slides[index].classList.add("active");
  currentSlide = index;

  // reset expand state on slide change
  expanded = false;

  productGrid.classList.remove("expanded");

  const text = exploreBtn.querySelector("span");
  if (text) text.textContent = "EXPLORE MORE";

  updateShopContent(index);
}

/* =========================
   TOGGLE EXPAND
========================= */

function toggleExpand() {
  expanded = !expanded;

  productGrid.classList.toggle("expanded", expanded);

  const text = exploreBtn.querySelector("span");
  if (text) {
    text.textContent = expanded ? "SHOW LESS" : "EXPLORE MORE";
  }

  updateShopContent(currentSlide);
}

/* =========================
   EVENTS
========================= */

if (exploreBtn) {
  exploreBtn.addEventListener("click", toggleExpand);
}

if (nextBtn) {
  nextBtn.addEventListener("click", () => {
    let next = currentSlide + 1;
    if (next >= slides.length) next = 0;
    showSlide(next);
  });
}

if (prevBtn) {
  prevBtn.addEventListener("click", () => {
    let prev = currentSlide - 1;
    if (prev < 0) prev = slides.length - 1;
    showSlide(prev);
  });
}

/* =========================
   SWIPE SUPPORT
========================= */

const heroContainer = document.querySelector(".shop-hero-container");

let touchStartX = 0;
let touchEndX = 0;

if (heroContainer) {
  heroContainer.addEventListener("touchstart", (e) => {
    touchStartX = e.changedTouches[0].screenX;
  });

  heroContainer.addEventListener("touchend", (e) => {
    touchEndX = e.changedTouches[0].screenX;

    const swipeDistance = touchStartX - touchEndX;

    // swipe left
    if (swipeDistance > 50) {
      let next = currentSlide + 1;
      if (next >= slides.length) next = 0;
      showSlide(next);
    }

    // swipe right
    if (swipeDistance < -50) {
      let prev = currentSlide - 1;
      if (prev < 0) prev = slides.length - 1;
      showSlide(prev);
    }
  });
}

const dots = document.querySelectorAll(".dot");

function showSlide(index) {
  slides.forEach((s) => s.classList.remove("active"));

  dots.forEach((dot) => dot.classList.remove("active"));

  if (!slides[index]) return;

  slides[index].classList.add("active");

  if (dots[index]) {
    dots[index].classList.add("active");
  }

  currentSlide = index;

  expanded = false;
  productGrid.classList.remove("expanded");

  const text = exploreBtn.querySelector("span");
  if (text) text.textContent = "EXPLORE MORE";

  updateShopContent(index);
}

dots.forEach((dot) => {
  dot.addEventListener("click", () => {
    showSlide(Number(dot.dataset.index));
  });
});

/* =========================
   INIT
========================= */

showSlide(0);
