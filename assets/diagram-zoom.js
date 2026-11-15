/* Irish School Maths: accessible enlargement for static PreTeXt diagrams.
   Embedded applications and iframes keep their own controls. */
(() => {
  "use strict";
  const selector = "main figure img, main .image-box img, main .figure img, .ptx-content figure img, main figure object[type='image/svg+xml']";
  let viewer, zoomImage, caption, status, pane, trigger, scale = 1;
  function ensureViewer() {
    if (viewer) return;
    viewer = document.createElement("dialog");
    viewer.className = "maths-diagram-viewer";
    viewer.setAttribute("aria-label", "Enlarged mathematics diagram");
    viewer.innerHTML = [
      '<div class="maths-diagram-controls">',
      '<strong class="maths-diagram-caption"></strong>',
      '<span class="maths-diagram-status" aria-live="polite"></span>',
      '<button type="button" data-zoom="out" aria-label="Zoom out">−</button>',
      '<button type="button" data-zoom="in" aria-label="Zoom in">+</button>',
      '<button type="button" data-zoom="reset">Reset</button>',
      '<button type="button" data-zoom="close" aria-label="Close enlarged diagram">Close ×</button>',
      '</div>',
      '<div class="maths-diagram-pane" tabindex="0" aria-label="Scroll to explore the enlarged diagram"><img alt="" /></div>'
    ].join("");
    caption = viewer.querySelector(".maths-diagram-caption");
    status = viewer.querySelector(".maths-diagram-status");
    pane = viewer.querySelector(".maths-diagram-pane");
    zoomImage = pane.querySelector("img");
    viewer.addEventListener("click", event => {
      const button = event.target.closest("button[data-zoom]");
      if (!button) return;
      const action = button.dataset.zoom;
      if (action === "close") viewer.close();
      else if (action === "reset") applyScale(1);
      else applyScale(scale + (action === "in" ? 0.25 : -0.25));
    });
    viewer.addEventListener("keydown", event => {
      if (event.target instanceof HTMLInputElement || event.target instanceof HTMLTextAreaElement) return;
      if (event.key === "+" || event.key === "=") { event.preventDefault(); applyScale(scale + 0.25); }
      if (event.key === "-") { event.preventDefault(); applyScale(scale - 0.25); }
      if (event.key === "0") { event.preventDefault(); applyScale(1); }
    });
    viewer.addEventListener("close", () => {
      zoomImage.removeAttribute("src");
      if (trigger && trigger.isConnected) trigger.focus();
    });
    document.body.appendChild(viewer);
  }
  function applyScale(value) {
    scale = Math.max(0.5, Math.min(4, Math.round(value * 4) / 4));
    zoomImage.style.width = Math.round(scale * 100) + "%";
    status.textContent = Math.round(scale * 100) + "%";
  }
  function openDiagram(original, sourceButton) {
    const source = original.currentSrc || original.getAttribute("src") || original.getAttribute("data") || "";
    if (!source || /^(javascript|data:text\/html):/i.test(source)) return;
    ensureViewer();
    trigger = sourceButton;
    const figure = original.closest("figure, .figure") || original.parentElement;
    const rawTitle = figure.querySelector("figcaption, .caption, .figure-caption");
    const name = original.getAttribute("alt") || original.getAttribute("aria-label") || "Mathematics diagram";
    caption.textContent = (rawTitle && rawTitle.textContent.trim()) || name;
    zoomImage.alt = name;
    zoomImage.src = source;
    applyScale(1);
    viewer.showModal();
    pane.scrollTop = 0;
    pane.scrollLeft = 0;
    viewer.querySelector('[data-zoom="close"]').focus();
  }
  function enhance() {
    for (const diagram of document.querySelectorAll(selector)) {
      if (diagram.dataset.mathsDiagramZoom === "1" || diagram.closest(".maths-diagram-viewer")) continue;
      const linked = diagram.closest("a");
      if (!diagram.currentSrc && !diagram.getAttribute("src") && !diagram.getAttribute("data")) continue;
      diagram.dataset.mathsDiagramZoom = "1";
      const button = document.createElement("button");
      button.type = "button";
      button.className = "maths-diagram-enlarge";
      button.textContent = "Enlarge diagram";
      button.setAttribute("aria-label", "Enlarge this mathematics diagram");
      button.addEventListener("click", () => openDiagram(diagram, button));
      (linked || diagram).insertAdjacentElement("afterend", button);
      if (!linked && diagram.tagName.toLowerCase() === "img") {
        diagram.classList.add("maths-diagram-clickable");
        diagram.addEventListener("click", () => openDiagram(diagram, button));
      }
    }
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", enhance, {once: true});
  else enhance();
  // Covers PreTeXt knowls opened after the page loads.
  let scheduled = false;
  const observer = new MutationObserver(() => {
    if (scheduled) return;
    scheduled = true;
    requestAnimationFrame(() => { scheduled = false; enhance(); });
  });
  observer.observe(document.documentElement, {childList: true, subtree: true});
})();