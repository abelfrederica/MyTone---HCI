const menuToggle = document.getElementById("menuToggle");
const sidebar = document.getElementById("sidebar");
const overlay = document.getElementById("sidebarOverlay");
const closeSidebar = document.getElementById("closeSidebar");

if (menuToggle && sidebar && overlay && closeSidebar) {
  menuToggle.addEventListener("click", () => {
    sidebar.classList.add("active");
    overlay.classList.add("active");
  });

  function closeMenu() {
    sidebar.classList.remove("active");
    overlay.classList.remove("active");
  }

  closeSidebar.addEventListener("click", closeMenu);
  overlay.addEventListener("click", closeMenu);
}
