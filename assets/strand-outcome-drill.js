/* Irish School Maths — progressive, accessible strand learning outcomes.
   Enhances NCCA outcome tables in place; never changes or removes source text.
   Drill down only when a numbered outcome contains several separately printed
   statements or subparts. No iframe and no separate assessment framework. */
(() => {
  "use strict";
  const strandInfo = {
    "jc-outcomes-number": ["Junior Cycle", "Number", 5],
    "jc-outcomes-geometry": ["Junior Cycle", "Geometry and Trigonometry", 6],
    "jc-outcomes-algebra": ["Junior Cycle", "Algebra and Functions", 7],
    "jc-outcomes-statistics": ["Junior Cycle", "Statistics and Probability", 3],
    "lc-ol-statistics-outcomes": ["Leaving Certificate · Ordinary Level", "Statistics and Probability", 7],
    "lc-ol-geometry-outcomes": ["Leaving Certificate · Ordinary Level", "Geometry and Trigonometry", 4],
    "lc-ol-number-outcomes": ["Leaving Certificate · Ordinary Level", "Number", 4],
    "lc-ol-algebra-outcomes": ["Leaving Certificate · Ordinary Level", "Algebra", 4],
    "lc-ol-functions-outcomes": ["Leaving Certificate · Ordinary Level", "Functions", 2]
  };
  function text(node) { return (node?.textContent || "").replace(/\s+/g, " ").trim(); }
  function safeClone(node) {
    const copy = node.cloneNode(true);
    if (copy.hasAttribute("id")) copy.removeAttribute("id");
    copy.querySelectorAll("[id]").forEach(el => el.removeAttribute("id"));
    copy.querySelectorAll(".autopermalink").forEach(el => el.remove());
    return copy;
  }
  function paragraphs(cell) {
    return [...cell.querySelectorAll(":scope > .para")];
  }
  function install() {
    for (const [sectionId, [course, strand, expected]] of Object.entries(strandInfo)) {
      const section = document.getElementById(sectionId);
      if (!section || section.dataset.drillInstalled === "yes") continue;
      const source = section.querySelector("figure.table table.tabular");
      if (!source) {console.warn("Learning outcome table not found:", sectionId); continue;}
      const outcomes = [];
      for (const row of source.querySelectorAll("tr")) {
        const cells = Array.from(row.children).filter(c => c.matches("td"));
        if (cells.length !== 2) continue;
        const label = paragraphs(cells[0])[0] || cells[0];
        const match = text(label).match(/^((?:N|GT|AF|SP|[1-5])\.\d+)$/);
        if (!match) continue;
        const statements = paragraphs(cells[1]);
        if (!statements.length) continue;
        const lead = paragraphs(cells[0])[1] || null;
        outcomes.push({code:match[1], heading:text(lead), row, labelCell:cells[0], statementCell:cells[1], statements});
      }
      if (outcomes.length !== expected) {
        console.warn("Outcome count does not match syllabus; leaving table untouched", sectionId, outcomes.length, expected);
        continue;
      }
      // Keep every original statement in the native table, including Maths markup.
      section.dataset.drillInstalled = "yes";
      section.classList.add("lo-drill-section");
      const dialog = document.createElement("dialog");
      dialog.className = "lo-drill-dialog";
      dialog.setAttribute("aria-label", course + ": " + strand + " learning outcome");
      dialog.innerHTML = [
        '<div class="lo-drill-header">',
          '<div class="lo-drill-context"></div>',
          '<button type="button" class="lo-drill-close" aria-label="Close learning outcome">Close ×</button>',
        '</div>',
        '<div class="lo-drill-scroll" tabindex="0">',
          '<h2 class="lo-drill-title"></h2>',
          '<div class="lo-drill-mode" role="group" aria-label="Reading mode">',
            '<button type="button" class="lo-drill-whole" aria-pressed="true">Complete outcome</button>',
            '<button type="button" class="lo-drill-parts" aria-pressed="false">One part at a time</button>',
          '</div>',
          '<div class="lo-drill-intro"></div>',
          '<div class="lo-drill-content"></div>',
          '<div class="lo-drill-part-controls" hidden>',
            '<button type="button" class="lo-drill-part-prev">← Previous part</button>',
            '<span class="lo-drill-part-count" aria-live="polite"></span>',
            '<button type="button" class="lo-drill-part-next">Next part →</button>',
          '</div>',
        '</div>',
        '<div class="lo-drill-footer">',
          '<button type="button" class="lo-drill-prev">← Previous outcome</button>',
          '<span class="lo-drill-count" aria-live="polite"></span>',
          '<button type="button" class="lo-drill-next">Next outcome →</button>',
        '</div>'
      ].join("");
      document.body.appendChild(dialog);
      const $ = sel => dialog.querySelector(sel);
      const title = $(".lo-drill-title"), content = $(".lo-drill-content"),
        intro = $(".lo-drill-intro"), wholeBtn = $(".lo-drill-whole"),
        partsBtn = $(".lo-drill-parts"), partBar = $(".lo-drill-part-controls"),
        prevPart = $(".lo-drill-part-prev"), nextPart = $(".lo-drill-part-next"),
        prev = $(".lo-drill-prev"), next = $(".lo-drill-next"),
        counter = $(".lo-drill-count"), partCounter = $(".lo-drill-part-count"),
        scroller = $(".lo-drill-scroll"), close = $(".lo-drill-close");
      $(".lo-drill-context").textContent = course + " · " + strand;
      let position = 0, part = 0, mode = "whole", trigger = null;
      function split(outcome) {
        const items = outcome.statements;
        // A single printed line, or a heading and one statement, has no
        // meaningful additional level. Preserve those in whole-outcome mode.
        if (items.length < 3) return null;
        const first = items[0];
        const hasLead = /(:|should be able to|so that they can)\s*$/i.test(text(first));
        const lead = hasLead ? first : null;
        const subparts = hasLead ? items.slice(1) : items.slice();
        return subparts.length >= 2 ? {lead, subparts} : null;
      }
      function appendClones(target, nodes) {
        target.replaceChildren(...nodes.map(safeClone));
      }
      function render() {
        const outcome = outcomes[position];
        const more = split(outcome);
        if (!more) mode = "whole";
        if (part >= (more?.subparts.length || 1)) part = 0;
        title.textContent = outcome.code + (outcome.heading ? " — " + outcome.heading : "");
        counter.textContent = (position + 1) + " of " + outcomes.length;
        prev.disabled = position === 0;
        next.disabled = position === outcomes.length - 1;
        partsBtn.hidden = !more;
        $(".lo-drill-mode").hidden = !more;
        wholeBtn.setAttribute("aria-pressed", String(mode === "whole"));
        partsBtn.setAttribute("aria-pressed", String(mode === "parts"));
        intro.replaceChildren();
        if (mode === "parts" && more) {
          if (more.lead) appendClones(intro, [more.lead]);
          appendClones(content, [more.subparts[part]]);
          partBar.hidden = false;
          partCounter.textContent = "Part " + (part + 1) + " of " + more.subparts.length;
          prevPart.disabled = part === 0;
          nextPart.disabled = part === more.subparts.length - 1;
        } else {
          appendClones(content, outcome.statements);
          partBar.hidden = true;
        }
        scroller.scrollTop = 0;
        // PreTeXt renders mathematics in the original table. The clone keeps
        // that markup; if MathJax hasn't run yet, give it a chance to typeset.
        if (window.MathJax?.typesetPromise && !content.querySelector("mjx-container"))
          window.MathJax.typesetPromise([content, intro]).catch(() => {});
      }
      function moveOutcome(offset) {
        const destination = position + offset;
        if (destination < 0 || destination >= outcomes.length) return;
        position = destination; part = 0; mode = "whole"; render();
      }
      outcomes.forEach((outcome, i) => {
        const open = document.createElement("button");
        open.type = "button";
        open.className = "lo-drill-open";
        open.textContent = "Enlarge " + outcome.code;
        open.setAttribute("aria-label", "Read complete learning outcome " + outcome.code);
        open.addEventListener("click", () => {
          trigger = open; position = i; part = 0; mode = "whole";
          render(); dialog.showModal(); close.focus();
        });
        outcome.labelCell.appendChild(open);
        // Also click the statement, without replacing the source HTML.
        outcome.statementCell.classList.add("lo-drill-clickable");
        outcome.statementCell.addEventListener("click", event => {
          if (event.target.closest("a,button") || window.getSelection()?.toString()) return;
          open.click();
        });
      });
      wholeBtn.addEventListener("click", () => {mode="whole"; render();});
      partsBtn.addEventListener("click", () => {mode="parts"; part=0; render();});
      prevPart.addEventListener("click", () => {if (part>0){part--;render();}});
      nextPart.addEventListener("click", () => {
        if (part<(split(outcomes[position])?.subparts.length||0)-1){part++;render();}
      });
      prev.addEventListener("click", () => moveOutcome(-1));
      next.addEventListener("click", () => moveOutcome(1));
      close.addEventListener("click", () => dialog.close());
      dialog.addEventListener("close", () => {if(trigger?.isConnected) trigger.focus();});
      dialog.addEventListener("keydown", event => {
        if (event.ctrlKey || event.altKey || event.metaKey ||
            event.target instanceof HTMLInputElement) return;
        if (event.key !== "ArrowLeft" && event.key !== "ArrowRight") return;
        // Normal arrows move subparts in step mode; Shift+arrow moves outcomes.
        event.preventDefault();
        const direction = event.key === "ArrowRight" ? 1 : -1;
        const more = split(outcomes[position]);
        if (mode === "parts" && more && !event.shiftKey) {
          part = Math.max(0,Math.min(more.subparts.length-1,part+direction));
          render();
        } else moveOutcome(direction);
      });
    }
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", install, {once:true});
  else install();
})();