/* Presentation belongs inside each individual JC / LC OL outcome section.
   Official content remains fully visible in the underlying page. */
(() => {
  "use strict";
  function install() {
    const section = document.querySelector('section[data-outcome-code]') || [...document.querySelectorAll('section[id^="jc-outcomes-algebra-af"]')]
      .find(el => /^jc-outcomes-algebra-af[1-7]$/.test(el.id));
    if (!section || section.dataset.outcomeSlides === "yes") return;
    const paragraphs = [...section.querySelectorAll(":scope > .para")]
      .filter(p => p.textContent.trim());
    if (!paragraphs.length) return;
    section.dataset.outcomeSlides = "yes";
    const code = section.dataset.outcomeCode || "AF." + section.id.match(/af([1-7])$/)[1];
    const course = section.dataset.outcomeCourse || "Junior Cycle";
    const group = section.dataset.outcomeGroup || "Algebra and Functions";
    const headingSource = section.querySelector(":scope > .heading, :scope > h2, :scope > h3");
    const title = headingSource?.textContent?.replace(/\s+/g, " ").trim() || code;
    const launcher = document.createElement("button");
    launcher.type = "button";
    launcher.className = "jc-algebra-slides-launch";
    launcher.textContent = "Present " + code + " as slides";
    launcher.setAttribute("aria-haspopup", "dialog");
    if (headingSource) headingSource.insertAdjacentElement("afterend", launcher);
    else section.prepend(launcher);

    const dialog = document.createElement("dialog");
    dialog.className = "jc-algebra-slides-dialog";
    dialog.setAttribute("aria-label", code + " presentation");
    dialog.innerHTML = [
      '<header class="jc-algebra-slide-head">',
      '<div><p class="jc-algebra-slide-kicker">Junior Cycle · Algebra and Functions</p>',
      '<p class="jc-algebra-slide-count" aria-live="polite"></p></div>',
      '<button type="button" class="jc-algebra-slide-close">Close ×</button>',
      '</header>',
      '<section class="jc-algebra-slide-scroll" tabindex="0">',
      '<h2 id="jc-algebra-slide-title"></h2>',
      '<div class="jc-algebra-slide-content"></div>',
      '</section>',
      '<footer class="jc-algebra-slide-foot">',
      '<button type="button" class="jc-algebra-slide-prev">← Previous</button>',
      '<button type="button" class="jc-algebra-slide-next">Next →</button>',
      '</footer>'
    ].join("");
    document.body.appendChild(dialog);
    const $ = q => dialog.querySelector(q);
    $(".jc-algebra-slide-kicker").textContent = course + " · " + group;
    const count = $(".jc-algebra-slide-count");
    const heading = $("#jc-algebra-slide-title");
    const content = $(".jc-algebra-slide-content");
    const scroller = $(".jc-algebra-slide-scroll");
    const previous = $(".jc-algebra-slide-prev");
    const next = $(".jc-algebra-slide-next");
    const close = $(".jc-algebra-slide-close");
    const example = section.querySelector(':scope > .remark');
    const slides = [paragraphs, ...paragraphs.map(p => [p])];
    if (example) slides.push([example]);
    let current = 0;
    function clone(node) {
      const copy = node.cloneNode(true);
      copy.removeAttribute("id");
      copy.querySelectorAll("[id]").forEach(el => el.removeAttribute("id"));
      copy.querySelectorAll(".autopermalink").forEach(el => el.remove());
      return copy;
    }
    function show(i) {
      current = Math.max(0, Math.min(slides.length - 1, i));
      count.textContent = (current === 0 ? "Complete outcome" :
        example && current === slides.length - 1 ? "Teaching example" : "Detail " + current) +
        " · " + (current + 1) + " of " + slides.length;
      heading.textContent = title;
      content.replaceChildren(...slides[current].map(clone));
      previous.disabled = current === 0;
      next.disabled = current === slides.length - 1;
      scroller.scrollTop = 0;
      if (window.MathJax?.typesetPromise && !content.querySelector("mjx-container"))
        window.MathJax.typesetPromise([content]).catch(() => {});
    }
    previous.addEventListener("click", () => show(current - 1));
    next.addEventListener("click", () => show(current + 1));
    close.addEventListener("click", () => dialog.close());
    launcher.addEventListener("click", () => { show(0); dialog.showModal(); close.focus(); });
    dialog.addEventListener("close", () => launcher.focus());
    dialog.addEventListener("keydown", event => {
      if (event.altKey || event.ctrlKey || event.metaKey || event.target.closest("a, input, select, textarea")) return;
      if (event.key === "ArrowRight") { event.preventDefault(); show(current + 1); }
      if (event.key === "ArrowLeft") { event.preventDefault(); show(current - 1); }
    });
  }
  if (document.readyState === "loading")
    document.addEventListener("DOMContentLoaded", install, {once:true});
  else install();
})();
