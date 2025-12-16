// assets/js/script.js

// --- GA lazy loader (only if gtag not present) ---
(function ensureGtag() {
  if (typeof window.gtag === 'function') return;
  // quick guard so we only inject once
  if (window._gtag_injected) return;
  window._gtag_injected = true;

  // Create script element for gtag.js
  var s = document.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=G-ES6BDQMP3K'; // use your measurement id
  s.onload = function() {
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    window.gtag = gtag;
    gtag('js', new Date());
    gtag('config', 'G-ES6BDQMP3K', { 'send_page_view': false });
    // note: send_page_view false so we don't duplicate pageview if GA added elsewhere
  };
  document.head.appendChild(s);
})();
// --- end gtag lazy loader ---

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

  function buildCard(root, previewUrl, fullUrl, meta = {}) {
    const card = document.createElement('article');
    card.className = 'wall-card';

    const thumb = document.createElement('div');
    thumb.className = 'wall-thumb';

    const img = document.createElement('img');
    const isDesktop = (typeof window !== 'undefined') && window.matchMedia('(min-width: 1024px)').matches;
    // Desktop collections: no lazy-loading per request; mobile/tablet keep lazy for bandwidth
    img.loading = isDesktop ? 'eager' : 'lazy';
    img.decoding = 'async';
    img.alt = 'Wallpaper preview';
    img.src = previewUrl;
    img.srcset = `${previewUrl} 1000w, ${fullUrl} 2160w`;
    img.sizes = '(min-width:1200px) 33vw, (min-width:700px) 50vw, 100vw';
    if (isDesktop && typeof meta.index === 'number' && meta.index < 6) {
      img.fetchPriority = 'high';
    }

    thumb.appendChild(img);

    // Analytics: fire thumb-click when user taps the preview
    img.addEventListener('click', () => {
      try {
        if (typeof gtag === 'function') {
          gtag('event', 'gallery_thumb_click', {
            category: meta.category || '(unknown)',
            file_name: meta.file_name || fullUrl.split('/').pop(),
            thumb_url: meta.thumb_url || previewUrl,
            full_url: meta.full_url || fullUrl
          });
        }
      } catch (e) { /* ignore analytics errors */ }
    });

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
        try {
          if (typeof gtag === 'function') {
            gtag('event', 'wallpaper_download', {
              category: meta.category || '(unknown)',
              file_name: meta.file_name || fullUrl.split('/').pop(),
              thumb_url: meta.thumb_url || previewUrl,
              full_url: meta.full_url || fullUrl
            });
          }
        } catch (e) { /* ignore analytics errors */ }
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

    // Fire thumbnail view event once when card enters viewport
    try {
      if (typeof IntersectionObserver === 'function') {
        const viewObs = new IntersectionObserver((entries, observer) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              try {
                if (typeof gtag === 'function') {
                  gtag('event', 'gallery_thumb_view', {
                    category: meta.category || '(unknown)',
                    file_name: meta.file_name || fullUrl.split('/').pop(),
                    thumb_url: meta.thumb_url || previewUrl,
                    full_url: meta.full_url || fullUrl
                  });
                }
              } catch (e) { /* ignore analytics errors */ }
              observer.unobserve(entry.target);
            }
          });
        }, { threshold: 0.5 });
        viewObs.observe(thumb);
      }
    } catch (e) { /* ignore observer errors */ }

    card.appendChild(thumb);
    card.appendChild(link);
    root.appendChild(card);
  }

  // Counters for summary
  let createdCount = 0;
  let missingCount = 0;

  const gallerySections = document.querySelectorAll('section[data-gallery-prefix]');
  gallerySections.forEach((section) => {
    const root = section.querySelector('[data-gallery-root]');
    if (!root) return;
    // Clear any statically-rendered cards to avoid duplicates when JS builds the grid.
    while (root.firstChild) root.removeChild(root.firstChild);
    const prefix = section.getAttribute('data-gallery-prefix');
    // Optional explicit list of filenames (comma-separated). When present
    // we iterate that list instead of using the numeric prefix+count scheme.
    const listAttr = section.getAttribute('data-gallery-list');
    const count = parseInt(section.getAttribute('data-gallery-count'), 10);
    const promises = [];

    const items = [];
    if (listAttr) {
      listAttr.split(',').map(s => s.trim()).filter(Boolean).forEach((name) => {
        // If the name already looks like a path, use it as-is; otherwise append to prefix
        if (name.indexOf('/') !== -1) items.push(name);
        else items.push(prefix + name);
      });
    } else {
      if (!prefix || !count || count <= 0) return;
      for (let i = 1; i <= count; i++) {
        const fileNum = String(i).padStart(2, '0');
        const base = `${prefix}${fileNum}`; // e.g. assets/wallpapers/abstract-01
        items.push(base);
      }
    }

    for (let idx = 0; idx < items.length; idx++) {
      const base = items[idx];
      // Prefer flattened thumbs folder (assets/wallpapers_thumbs/<basename>),
      // then fallback to possible subfolder thumbs and finally full images.
      const basename = base.split('/').pop().replace(/\.(jpg|jpeg|png)$/i, '');
      const flatThumb = `assets/wallpapers_thumbs/${basename}.jpg`;
      const thumbCandidateJpg = base.replace('/wallpapers/', '/wallpapers_thumbs/') + (base.match(/\.(jpg|jpeg|png)$/i) ? '' : '.jpg');
      const candidates = [
        flatThumb,
        thumbCandidateJpg,
        // If base already contains an extension use it, otherwise try common ones
        ...(base.match(/\.(jpg|jpeg|png)$/i) ? [base] : [base + '.jpg', base + '.jpeg', base + '.png'])
      ];

      const p = testImageCandidates(candidates)
        .then((foundUrl) => {
          createdCount++;
          // Derive category and file_name for analytics
          let category = '(unknown)';
          try {
            const m = prefix.match(/wallpapers\/([^\/\-]+)/i);
            if (m && m[1]) category = m[1];
            else {
              const parts = prefix.split('/').filter(Boolean);
              category = parts[parts.length - 1] || category;
            }
          } catch (e) { /* ignore */ }
          const hasExtension = /\.[a-zA-Z0-9]+$/.test(base);
          const fileName = base.split('/').pop() || '';
          const fullUrl = hasExtension ? base : `${base}.jpg`;
          const meta = { category, file_name: hasExtension ? fileName : `${fileName}.jpg`, thumb_url: foundUrl, full_url: fullUrl, index: idx };
          buildCard(root, foundUrl, fullUrl, meta);
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
