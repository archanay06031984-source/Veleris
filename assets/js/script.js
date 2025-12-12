// assets/js/script.js

document.addEventListener("DOMContentLoaded", () => {
  // Simple reveal (keep existing behavior)
  const revealEls = document.querySelectorAll(".reveal");
  if (revealEls.length) {
    const obs = new IntersectionObserver(
      (entries, observer) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.16 }
    );
    revealEls.forEach((el) => obs.observe(el));
  }

  // Highlights slider (keeps original behavior)
  const sets = Array.from(document.querySelectorAll(".highlight-set"));
  const prevBtn = document.querySelector("[data-highlight-prev]");
  const nextBtn = document.querySelector("[data-highlight-next]");

  if (sets.length && prevBtn && nextBtn) {
    let current = 0;
    const clearAnim = (el) => el.classList.remove("slide-in-right","slide-in-left","slide-out-right","slide-out-left");
    const goTo = (nextIndex, direction) => {
      if (nextIndex === current) return;
      const cur = sets[current];
      const next = sets[nextIndex];
      clearAnim(cur); clearAnim(next);
      cur.classList.remove("active");
      cur.classList.add(direction === "next" ? "slide-out-left" : "slide-out-right");
      next.classList.add("active");
      next.classList.add(direction === "next" ? "slide-in-right" : "slide-in-left");
      current = nextIndex;
    };
    sets.forEach((s, idx) => s.classList.toggle("active", idx === 0));
    prevBtn.addEventListener("click", () => goTo((current - 1 + sets.length) % sets.length, "prev"));
    nextBtn.addEventListener("click", () => goTo((current + 1) % sets.length, "next"));
  }

  /* COLLECTION GALLERIES
     - Build cards only when a preview image exists
     - Prefer thumbnails in /assets/wallpapers_thumbs/
     - Use <img loading="lazy"> for previews
     - Download button fetches full-res as blob and forces a download
     - Log summary of created vs missing slots
  */

  function testImageCandidates(candidates = []) {
    return new Promise((resolve, reject) => {
      let i = 0;
      const tryNext = () => {
        if (i >= candidates.length) {
          reject(new Error('no candidate loaded'));
          return;
        }
        const src = candidates[i];
        const img = new Image();
        img.onload = () => resolve(src);
        img.onerror = () => { i++; tryNext(); };
        img.src = src;
      };
      tryNext();
    });
  }

  function buildCard(root, previewUrl, fullUrl) {
    const card = document.createElement('article');
    card.className = 'wall-card';

    const thumb = document.createElement('div');
    thumb.className = 'wall-thumb';

    const img = document.createElement('img');
    img.loading = 'lazy';
    img.decoding = 'async';
    img.alt = 'Wallpaper preview';
    img.src = previewUrl;
    img.srcset = `${previewUrl} 1000w, ${fullUrl} 2160w`;
    img.sizes = '(min-width:1200px) 33vw, (min-width:700px) 50vw, 100vw';

    thumb.appendChild(img);

    const link = document.createElement('a');
    link.className = 'wall-link';
    link.href = fullUrl;
    link.setAttribute('aria-label', 'Download wallpaper');
    link.setAttribute('download', fullUrl.split('/').pop());

    const overlay = document.createElement('div');
    overlay.className = 'wall-overlay';

    const pill = document.createElement('button');
    pill.type = 'button';
    pill.className = 'download-pill';
    pill.textContent = 'Download';

    pill.addEventListener('click', async (e) => {
      e.preventDefault();
      try {
        const res = await fetch(fullUrl, { mode: 'cors' });
        if (!res.ok) throw new Error('fetch failed');
        const blob = await res.blob();
        const blobUrl = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = blobUrl;
        a.download = fullUrl.split('/').pop();
        document.body.appendChild(a);
        a.click();
        a.remove();
        URL.revokeObjectURL(blobUrl);
      } catch (err) {
        // last-resort fallback: attempt normal download link (will open in new tab in some browsers)
        const a = document.createElement('a');
        a.href = fullUrl;
        a.download = fullUrl.split('/').pop();
        document.body.appendChild(a);
        a.click();
        a.remove();
      }
    });

    overlay.appendChild(pill);
    link.appendChild(overlay);

    card.appendChild(thumb);
    card.appendChild(link);
    root.appendChild(card);
  }

  // Counters for summary
  let createdCount = 0;
  let missingCount = 0;

  const gallerySections = document.querySelectorAll('section[data-gallery-prefix][data-gallery-count]');
  gallerySections.forEach((section) => {
    const root = section.querySelector('[data-gallery-root]');
    if (!root) return;

    const prefix = section.getAttribute('data-gallery-prefix');
    const count = parseInt(section.getAttribute('data-gallery-count'), 10);
    if (!prefix || !count || count <= 0) return;

    const promises = [];

    for (let i = 1; i <= count; i++) {
      const fileNum = String(i).padStart(2, '0');
      const base = `${prefix}${fileNum}`; // e.g. assets/wallpapers/abstract-01
      const thumbCandidateJpg = base.replace('/wallpapers/', '/wallpapers_thumbs/') + '.jpg';
      const candidates = [
        thumbCandidateJpg,
        base + '.jpg',
        base + '.jpeg',
        base + '.png'
      ];

      const p = testImageCandidates(candidates)
        .then((foundUrl) => {
          createdCount++;
          buildCard(root, foundUrl, base + '.jpg');
        })
        .catch(() => {
          missingCount++;
          // fail quietly
        });

      promises.push(p);
    }

    // After all slots attempted, log summary for this section
    Promise.allSettled(promises).then(() => {
      console.log(`Gallery summary: ${createdCount} cards created, ${missingCount} missing`);
    });
  });

});
