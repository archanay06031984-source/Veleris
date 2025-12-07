// YEAR IN FOOTER (SAFE EVEN IF NOT PRESENT)
const yearSpan = document.getElementById("year");
if (yearSpan) {
  yearSpan.textContent = new Date().getFullYear();
}

// SCROLL REVEAL
const revealEls = document.querySelectorAll(".reveal");
if (revealEls.length) {
  const obs = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          obs.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.2 }
  );

  revealEls.forEach((el) => obs.observe(el));
}

// HIGHLIGHTS CAROUSEL
const highlightCards = document.querySelectorAll(".highlight-card");
const highlightRow = document.querySelector(".highlights-row");
const prevBtn = document.querySelector(".highlight-nav.prev");
const nextBtn = document.querySelector(".highlight-nav.next");

if (highlightCards.length && highlightRow && prevBtn && nextBtn) {
  const highlightData = [
    { image: "assets/wallpapers/minimal/minimal-1.jpg" },
    { image: "assets/wallpapers/anime/anime-1.jpg" },
    { image: "assets/wallpapers/cars/lamborghini/lamborghini-1.jpg" },
    { image: "assets/wallpapers/abstract/abstract-1.jpg" },
    { image: "assets/wallpapers/nature/nature-1.jpg" },
    { image: "assets/wallpapers/gradient/gradient-1.jpg" },
  ];

  let startIndex = 0;
  let isAnimating = false;

  function renderHighlights() {
    highlightCards.forEach((card, i) => {
      const thumb = card.querySelector(".highlight-thumb");
      const data = highlightData[(startIndex + i) % highlightData.length];
      if (thumb && data) {
        thumb.style.backgroundImage = `url('${data.image}')`;
      }

      card.classList.remove("center");
      if (i === 1) card.classList.add("center");
    });
  }

  function shift(dir) {
    if (isAnimating) return;
    isAnimating = true;

    highlightRow.classList.add(dir === "next" ? "slide-next" : "slide-prev");

    setTimeout(() => {
      startIndex =
        dir === "next"
          ? (startIndex + 1) % highlightData.length
          : (startIndex - 1 + highlightData.length) % highlightData.length;

      renderHighlights();
      highlightRow.classList.remove("slide-next", "slide-prev");
      isAnimating = false;
    }, 220);
  }

  prevBtn.addEventListener("click", () => shift("prev"));
  nextBtn.addEventListener("click", () => shift("next"));

  renderHighlights();
}
