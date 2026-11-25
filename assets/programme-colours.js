/* Native PreTeXt sidebar colour hierarchy.
   Chapter-to-programme mapping is generated from source/main.ptx at build time. */
(() => {
  "use strict";
  const partTargets = {
    "part-jc-introduction.html":"assessment",
    "part-jc-number.html":"number",
    "part-jc-geometry.html":"geometry",
    "part-jc-algebra.html":"algebra",
    "part-jc-statistics.html":"statistics",
    "part-jc-assessment.html":"assessment",
    "part-transition-year.html":"assessment",
    "part-lc-ol-introduction.html":"assessment",
    "part-lc-ol-statistics.html":"statistics",
    "part-lc-ol-geometry.html":"geometry",
    "part-lc-ol-number.html":"number",
    "part-lc-ol-algebra.html":"algebra",
    "part-lc-ol-functions.html":"algebra",
    "part-lc-hl-introduction.html":"assessment",
    "part-lc-hl-statistics.html":"statistics",
    "part-lc-hl-geometry.html":"geometry",
    "part-lc-hl-number.html":"number",
    "part-lc-hl-algebra.html":"algebra",
    "part-lc-hl-functions.html":"algebra"
  };
  const chapterTargets = __MATHS_CHAPTERS__;
  const tocSelector = "nav, .toc, .ptx-toc, .toc-container, #toc, .toc-items, .toc-item-list, [role='navigation']";
  const rowSelector = ".toc-title-box, .toc-item-title, .tocitem-title, .tocitem-heading";

  function setRowClass(link, role, programme) {
    const row = link.closest(rowSelector) || link.parentElement;
    // Never colour a container that contains a whole subtree of chapters/sections.
    if (!row || row.querySelectorAll("a[href]").length !== 1) return;
    row.classList.add("maths-"+role+"-container", "maths-programme-"+programme);
  }
  function paint() {
    const links = document.querySelectorAll("a[href]");
    links.forEach(link => {
      if (!link.closest(tocSelector)) return;
      let file;
      try { file = new URL(link.href, document.baseURI).pathname.split("/").pop(); }
      catch { return; }
      const part = partTargets[file];
      const chapter = chapterTargets[file];
      // Colour the existing U.1–U.13 links without adding extra navigation levels.
      const uMatch = /^jc-outcomes-unifying-u(\d{1,2})\.html$/.exec(file);
      if (uMatch) {
        const n = Number(uMatch[1]);
        const group = n <= 3 ? "blocks" : n === 4 ? "representation"
          : n <= 6 ? "connections" : n <= 10 ? "problems"
          : n <= 12 ? "proof" : "communication";
        link.classList.add("maths-unifying-outcome", "maths-unifying-"+group);
      }
      if (part) {
        if (!link.classList.contains("maths-programme-link")) {
          link.classList.add("maths-programme-link", "maths-programme-"+part);
          setRowClass(link, "programme", part);
        }
      } else if (chapter) {
        if (!link.classList.contains("maths-chapter-link")) {
          link.classList.add("maths-chapter-link", "maths-programme-"+chapter);
          setRowClass(link, "chapter", chapter);
        }
      }
    });
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", paint, {once:true});
  } else {
    paint();
  }
})();
