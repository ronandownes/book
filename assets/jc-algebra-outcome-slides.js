/* Seven-slide view for the Junior Cycle Algebra and Functions outcomes. */
(() => {
  "use strict";

  const cleanClone = node => {
    const clone = node.cloneNode(true);
    clone.querySelectorAll(".autopermalink").forEach(el => el.remove());
    clone.querySelectorAll("[id]").forEach(el => el.removeAttribute("id"));
    return clone;
  };

  function install() {
    const section = document.getElementById("jc-outcomes-algebra");
    const table = section?.querySelector("figure.table table.tabular");
    if (!section || !table) return;

    const outcomes = [];
    for (const row of table.querySelectorAll("tr")) {
      const cells = [...row.children].filter(cell => cell.matches("td"));
      if (cells.length !== 2) continue;
      const code = (cells[0].textContent || "").match(/\b(AF\.\d+)\b/)?.[1];
      if (code) outcomes.push({code, label:cells[0], content:cells[1], row});
    }
    if (outcomes.length !== 7 || outcomes.some((item, i) => item.code !== `AF.${i+1}`)) return;

    const launcher = document.createElement("button");
    launcher.type = "button";
    launcher.className = "jc-algebra-slides-launch";
    launcher.textContent = "Explore the 7 Algebra outcomes";
    launcher.setAttribute("aria-haspopup", "dialog");
    (table.closest("figure.table") || table).before(launcher);

    const dialog = document.createElement("dialog");
    dialog.className = "jc-algebra-slides-dialog";
    dialog.setAttribute("aria-labelledby", "jc-algebra-slide-title");
    dialog.innerHTML = `
      <header class="jc-algebra-slide-head">
        <div><p class="jc-algebra-slide-kicker">Junior Cycle · Algebra and Functions</p><p class="jc-algebra-slide-count" aria-live="polite"></p></div>
        <button type="button" class="jc-algebra-slide-close" aria-label="Close slides">Close ×</button>
      </header>
      <nav class="jc-algebra-slide-nav" aria-label="Choose an outcome slide"></nav>
      <section class="jc-algebra-slide-scroll" tabindex="0">
        <h2 id="jc-algebra-slide-title"></h2>
        <div class="jc-algebra-slide-content"></div>
        <button type="button" class="jc-algebra-slide-drill" hidden>Drill down closer into AF.3</button>
      </section>
      <footer class="jc-algebra-slide-foot">
        <button type="button" class="jc-algebra-slide-prev">← Previous slide</button>
        <button type="button" class="jc-algebra-slide-next">Next slide →</button>
      </footer>`;
    document.body.appendChild(dialog);

    const nav = dialog.querySelector(".jc-algebra-slide-nav");
    const count = dialog.querySelector(".jc-algebra-slide-count");
    const heading = dialog.querySelector("#jc-algebra-slide-title");
    const content = dialog.querySelector(".jc-algebra-slide-content");
    const scroller = dialog.querySelector(".jc-algebra-slide-scroll");
    const previous = dialog.querySelector(".jc-algebra-slide-prev");
    const next = dialog.querySelector(".jc-algebra-slide-next");
    const close = dialog.querySelector(".jc-algebra-slide-close");
    const drill = dialog.querySelector(".jc-algebra-slide-drill");
    const slideButtons = outcomes.map((outcome, i) => {
      const button = document.createElement("button");
      button.type = "button";
      button.textContent = String(i + 1);
      button.setAttribute("aria-label", `Open slide ${i+1}: ${outcome.code}`);
      button.addEventListener("click", () => render(i));
      nav.appendChild(button);
      return button;
    });
    let position = 0;
    let returnToSlides = false;

    function render(index) {
      position = Math.max(0, Math.min(outcomes.length - 1, index));
      const outcome = outcomes[position];
      const title = [...outcome.label.querySelectorAll(":scope > .para")][1];
      const titleText = title ? cleanClone(title).textContent.trim() : "";
      heading.textContent = outcome.code + (titleText ? " — " + titleText : "");
      count.textContent = `Slide ${position+1} of 7`;
      slideButtons.forEach((button, i) => {
        button.setAttribute("aria-current", String(i === position));
      });
      previous.disabled = position === 0;
      next.disabled = position === outcomes.length - 1;
      content.replaceChildren(...[...outcome.content.children]
        .filter(el => el.matches(".para"))
        .map(cleanClone));
      drill.hidden = position !== 2;
      scroller.scrollTop = 0;
      if (window.MathJax?.typesetPromise) window.MathJax.typesetPromise([heading, content]).catch(() => {});
    }

    previous.addEventListener("click", () => render(position - 1));
    next.addEventListener("click", () => render(position + 1));
    close.addEventListener("click", () => dialog.close());
    launcher.addEventListener("click", () => { render(0); dialog.showModal(); slideButtons[0].focus(); });
    dialog.addEventListener("close", () => launcher.focus());
    dialog.addEventListener("keydown", event => {
      if (event.altKey || event.ctrlKey || event.metaKey || event.target.closest("button")) return;
      if (event.key === "ArrowRight") { event.preventDefault(); render(position + 1); }
      if (event.key === "ArrowLeft") { event.preventDefault(); render(position - 1); }
    });

    drill.addEventListener("click", () => {
      const detailButton = outcomes[2].label.querySelector(".lo-drill-open");
      const detailDialog = document.querySelector("dialog.lo-drill-dialog");
      if (!detailButton || !detailDialog) return;
      returnToSlides = true;
      detailDialog.addEventListener("close", () => {
        if (returnToSlides) { returnToSlides = false; dialog.showModal(); slideButtons[2].focus(); }
      }, {once:true});
      dialog.close();
      window.setTimeout(() => detailButton.click(), 0);
    });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", install, {once:true});
  else install();
})();
