/* Native, progressive enhancement of the PreTeXt Unifying Strand table.
   The 13 official outcomes live only in source/jc-introduction.ptx, not in JavaScript.
   Without scripts, the complete table is still readable. */
(() => {
  "use strict";
  function init() {
    const root = document.getElementById("jc-unifying-table");
    if (!root || root.dataset.jcOutcomesEnhanced === "yes") return;
    const table = root.tagName.toLowerCase() === "table" ? root : root.querySelector("table");
    if (!table) return;
    const list = [];
    let group = "";
    for (const row of Array.from(table.querySelectorAll("tr"))) {
      const cells = Array.from(row.children).filter(el => /^(TD|TH)$/.test(el.tagName));
      if (cells.length !== 2) continue;
      const code = cells[0].textContent.trim().replace(/\s+/g, "");
      if (/^U\.(?:[1-9]|1[0-3])$/.test(code)) {
        list.push({code, group, cell: cells[1], text: cells[1].textContent.trim().replace(/\s+/g, " ")});
      } else if (/^(Building blocks|Representation|Connections|Problem solving|Generalisation and proof|Communication)$/i.test(cells[0].textContent.trim()) && cells[0].getAttribute("colspan") === "2") {
        group = cells[0].textContent.trim();
      } else if (cells[0].getAttribute("colspan") === "2") {
        group = cells[0].textContent.trim();
      }
    }
    if (list.length !== 13 || list.some((item, i) => item.code !== "U." + (i+1)) || list.some(item => !item.group || !item.text)) {
      console.warn("JC Unifying table was not enhanced: incomplete or incorrectly parsed outcomes.");
      return;
    }
    root.dataset.jcOutcomesEnhanced = "yes";
    root.classList.add("jc-unifying-native");
    const viewer = document.createElement("dialog");
    viewer.className = "jc-outcome-dialog";
    viewer.setAttribute("aria-labelledby", "jc-outcome-heading");
    viewer.setAttribute("aria-describedby", "jc-outcome-text");
    viewer.innerHTML = [
      '<div class="jc-outcome-modal-inner">',
      '<div class="jc-outcome-overline">Junior Cycle Mathematics · Unifying Strand</div>',
      '<h2 id="jc-outcome-heading"></h2>',
      '<p id="jc-outcome-text"></p>',
      '<div class="jc-outcome-modal-controls">',
      '<button type="button" data-action="previous">← Previous</button>',
      '<span class="jc-outcome-count" aria-live="polite"></span>',
      '<button type="button" data-action="next">Next →</button>',
      '<button type="button" data-action="close">Close ×</button>',
      '</div></div>'
    ].join("");
    document.body.appendChild(viewer);
    const heading = viewer.querySelector("#jc-outcome-heading");
    const statement = viewer.querySelector("#jc-outcome-text");
    const counter = viewer.querySelector(".jc-outcome-count");
    const previous = viewer.querySelector('[data-action="previous"]');
    const next = viewer.querySelector('[data-action="next"]');
    const close = viewer.querySelector('[data-action="close"]');
    let index = 0, origin = null;
    function show(i) {
      index = Math.max(0, Math.min(list.length-1, i));
      const item = list[index];
      heading.textContent = item.code + " — " + item.group;
      statement.textContent = item.text;
      counter.textContent = (index+1) + " of " + list.length;
      previous.disabled = index === 0;
      next.disabled = index === list.length-1;
    }
    list.forEach((item, i) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "jc-outcome-trigger";
      button.textContent = item.text;
      button.setAttribute("aria-label", "Read " + item.code + " in detail");
      button.addEventListener("click", () => {
        origin = button;
        show(i);
        viewer.showModal();
        close.focus();
      });
      item.cell.replaceChildren(button);
    });
    previous.addEventListener("click", () => show(index-1));
    next.addEventListener("click", () => show(index+1));
    close.addEventListener("click", () => viewer.close());
    viewer.addEventListener("close", () => {if(origin && origin.isConnected) origin.focus();});
    viewer.addEventListener("keydown", event => {
      if(event.altKey || event.ctrlKey || event.metaKey) return;
      if(event.key === "ArrowLeft") {event.preventDefault(); show(index-1);}
      if(event.key === "ArrowRight") {event.preventDefault(); show(index+1);}
    });
  }
  if(document.readyState === "loading") document.addEventListener("DOMContentLoaded", init, {once:true});
  else init();
})();