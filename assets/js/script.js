// assets/js/script.js

document.addEventListener("DOMContentLoaded", function () {
  /* =========================
     SCROLL REVEAL
     ========================= */
  var revealEls = document.querySelectorAll(".reveal");

  if (revealEls.length) {
    if ("IntersectionObserver" in window) {
      var observer = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) {
              entry.target.classList.add("visible");
              observer.unobserve(entry.target);
            }
          });
        },
        { threshold: 0.16 }
      );

      revealEls.forEach(function (el) {
        observer.observe(el);
      });
    } else {
      // Fallback: just show everything if IO not supported
      revealEls.forEach(function (el) {
        el.classList.add("visible");
      });
    }
  }

  /* =========================
     HIGHLIGHTS SLIDER (HOME)
     ========================= */
  var sets = Array.prototype.slice.call(
    document.querySelectorAll(".highlight-set")
  );
  var prevBtn = document.querySelector("[data-highlight-prev]");
  var nextBtn = document.querySelector("[data-highlight-next]");

  if (sets.length && prevBtn && nextBtn) {
    var current = 0;
    var isAnimating = false;

    function clearAnimClasses(el) {
      el.classList.remove(
        "slide-in-right",
        "slide-in-left",
        "slide-out-right",
        "slide-out-left"
      );
    }

    function goTo(nextIndex, direction) {
      if (nextIndex === current || isAnimating) return;

      var currentSet = sets[current];
      var nextSet = sets[nextIndex];

      isAnimating = true;

      clearAnimClasses(currentSet);
      clearAnimClasses(nextSet);

      currentSet.classList.remove("active");
      currentSet.classList.add(
        direction === "next" ? "slide-out-left" : "slide-out-right"
      );

      nextSet.classList.add("active");
      nextSet.classList.add(
        direction === "next" ? "slide-in-right" : "slide-in-left"
      );

      // End animation lock after duration (keeps clicks from spamming)
      setTimeout(function () {
        clearAnimClasses(currentSet);
        clearAnimClasses(nextSet);
        isAnimating = false;
      }, 460);
      current = nextIndex;
    }

    // only first active on load
    sets.forEach(function (set, idx) {
      set.classList.toggle("active", idx === 0);
    });

    prevBtn.addEventListener("click", function () {
      var nextIndex = (current - 1 + sets.length) % sets.length;
      goTo(nextIndex, "prev");
    });

    nextBtn.addEventListener("click", function () {
      var nextIndex = (current + 1) % sets.length;
      goTo(nextIndex, "next");
    });
  }

  /* =========================
     COLLECTION GALLERIES
     - tries .jpg → .jpeg → .png
     - only creates card if an image exists
     ========================= */

  var gallerySections = document.querySelectorAll(
    "section[data-gallery-prefix][data-gallery-count]"
  );

  gallerySections.forEach(function (section) {
    var root = section.querySelector("[data-gallery-root]");
    if (!root) return;

    var prefix = section.getAttribute("data-gallery-prefix") || "";
    var countAttr = section.getAttribute("data-gallery-count") || "0";
    var count = parseInt(countAttr, 10);

    if (!count || count <= 0) return;

    for (var i = 1; i <= count; i++) {
      (function (orderIndex) {
        var indexStr = String(orderIndex).padStart(2, "0"); // "01"
        var basePath = prefix + indexStr;                   // e.g. abstract-01
        var exts = [".jpg", ".jpeg", ".png"];
        var candidateIndex = 0;
        var testImg = new Image();

        function tryNext() {
          if (candidateIndex >= exts.length) {
            // no working file → no card, no blank tile
            return;
          }
          testImg.src = basePath + exts[candidateIndex];
        }

        testImg.onload = function () {
          var chosenPath = basePath + exts[candidateIndex];

          // Build card ONLY after we know this file exists
          var card = document.createElement("article");
          card.className = "wall-card";

          var thumb = document.createElement("div");
          thumb.className = "wall-thumb";
          thumb.style.backgroundImage = 'url("' + chosenPath + '")';

          var link = document.createElement("a");
          link.className = "wall-link";
          link.href = chosenPath;
          link.setAttribute("download", chosenPath.split("/").pop());
          link.setAttribute("aria-label", "Download wallpaper");

          var overlay = document.createElement("div");
          overlay.className = "wall-overlay";

          var pill = document.createElement("button");
          pill.type = "button";
          pill.className = "download-pill";
          pill.textContent = "Download";

          pill.addEventListener("click", function (e) {
            e.preventDefault();
            link.click(); // uses <a download> so it should download instead of open
          });

          overlay.appendChild(pill);
          link.appendChild(overlay);
          card.appendChild(thumb);
          card.appendChild(link);
          root.appendChild(card);
        };

        testImg.onerror = function () {
          candidateIndex += 1;
          tryNext();
        };

        // start with .jpg
        tryNext();
      })(i);
    }
  });
});