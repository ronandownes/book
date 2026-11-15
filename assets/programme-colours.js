/* Native PreTeXt sidebar colour hierarchy.
   Chapter-to-programme mapping is generated from source/main.ptx at build time. */
(() => {
  "use strict";
  const partTargets = {
    "part-junior-cycle.html":"jc",
    "part-transition-year.html":"ty",
    "part-leaving-certificate.html":"lc",
    "part-foundation.html":"foundation",
    "part-leaving-certificate-applied.html":"lca",
    "part-official-appendices.html":"appendices"
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
