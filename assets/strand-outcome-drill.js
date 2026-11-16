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
  function text(node) {
    if (!node) return "";
    const clone = node.cloneNode(true);
    clone.querySelectorAll(".autopermalink").forEach(el => el.remove());
    return (clone.textContent || "").replace(/\s+/g, " ").trim();
  }
  function safeClone(node) {
    const copy = node.cloneNode(true);
    if (copy.hasAttribute("id")) copy.removeAttribute("id");
    copy.querySelectorAll("[id]").forEach(el => el.removeAttribute("id"));
    copy.querySelectorAll(".autopermalink").forEach(el => el.remove());
    return copy;
  }
  // Segment long syllabus paragraphs while preserving their original DOM/MathJax.
  // A split is allowed at roman-numbered steps, semicolons separating
  // equations, or sufficiently distant prose commas. We never split at '='
  // or inside an actual MathJax/MathML expression.
  function detailPieces(source) {
    const paragraph = safeClone(source);
    const walker = document.createTreeWalker(paragraph, NodeFilter.SHOW_TEXT, {
      acceptNode(node) {
        return node.parentElement?.closest("mjx-container, math, svg, .MathJax, .katex")
          ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT;
      }
    });
    let raw = "";
    const at = [];
    let node;
    while ((node = walker.nextNode())) {
      const value = node.nodeValue || "";
      for (let i = 0; i < value.length; i++) {
        raw += value[i];
        at.push({node, offset:i});
      }
    }
    if (raw.length < 150) return [paragraph];
    const cuts = new Set([0, raw.length]);
    // Mark the *start* of successive i., ii., iii., iv. ... steps.
    const roman = /(?:^|[\s:;])(?:viii|vii|vi|iv|iii|ii|v|i)\.\s+(?=[A-Za-z])/gi;
    for (const m of raw.matchAll(roman)) {
      const position = m.index + (/^[\s:;]/.test(m[0]) ? 1 : 0);
      if (position > 24 && position < raw.length - 8) cuts.add(position);
    }
    // Semicolons generally delimit consecutive equations. Include the
    // semicolon in the preceding statement for faithful punctuation.
    for (let i = 0; i < raw.length - 1; i++) {
      if (raw[i] === ";" && /\S/.test(raw.slice(i+1))) cuts.add(i+1);
    }
    const major = [...cuts].sort((a,b)=>a-b);
    for (let i = 1; i < major.length; i++) {
      const from = major[i-1], to = major[i];
      // On long prose clauses, use commas *with a following space*. Do not
      // split coordinates (1,2), mathematical lists a,b, or very short parts.
      if (to - from < 130) continue;
      let last = from;
      for (let p = from + 1; p < to - 20; p++) {
        if (raw[p] === "," && /\s/.test(raw[p+1] || "") && p-last >= 85) {
          cuts.add(p+1);
          last = p+1;
        }
      }
    }
    let boundaries = [...cuts].sort((a,b)=>a-b);
    // Avoid lonely tails and single-symbol cards.
    for (let i = boundaries.length-2; i > 0; i--) {
      if (boundaries[i+1] - boundaries[i] < 22) boundaries.splice(i,1);
    }
    if (boundaries.length < 3) return [paragraph];
    const result = [];
    for (let i=0; i<boundaries.length-1; i++) {
      const from=boundaries[i], to=boundaries[i+1];
      if (from >= to || !at[from] || !at[to-1]) continue;
      const selection = document.createRange();
      selection.setStart(at[from].node,at[from].offset);
      selection.setEnd(at[to-1].node,at[to-1].offset+1);
      const part = document.createElement("div");
      part.className = "para lo-drill-piece";
      part.appendChild(selection.cloneContents());
      part.querySelectorAll(".autopermalink,[id]").forEach(el=>el.removeAttribute("id"));
      result.push(part);
    }
    return result.length >= 2 ? result : [paragraph];
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
        const match = text(label).match(/^((?:N|GT|AF|SP|[1-5])\.\d+)(?=\D|$)/);
        if (!match) continue;
        const statements = paragraphs(cells[1]);
        if (!statements.length) continue;
        const lead = paragraphs(cells[0])[1] || null;
        const heading = text(lead).replace(new RegExp("^" + match[1].replace(".", "\\.") + "\\s*"), "");
        outcomes.push({code:match[1], heading, row, labelCell:cells[0], statementCell:cells[1], statements});
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
            '<button type="button" class="lo-drill-parts" aria-pressed="false">By letter / part</button>',
            '<button type="button" class="lo-drill-subparts" aria-pressed="false" hidden>By roman numeral</button>',
            '<button type="button" class="lo-drill-details" aria-pressed="false" hidden>By equation</button>',
          '</div>',
          '<div class="lo-drill-intro"></div>',
          '<div class="lo-drill-content"></div>',
          '<div class="lo-drill-part-controls" hidden>',
            '<button type="button" class="lo-drill-part-prev">← Previous part</button>',
            '<span class="lo-drill-part-count" aria-live="polite"></span>',
            '<button type="button" class="lo-drill-part-next">Next part →</button>',
          '</div>',
          '<div class="lo-drill-subpart-controls" hidden>',
            '<button type="button" class="lo-drill-subpart-prev">← Previous subpart</button>',
            '<span class="lo-drill-subpart-count" aria-live="polite"></span>',
            '<button type="button" class="lo-drill-subpart-next">Next subpart →</button>',
          '</div>',
          '<div class="lo-drill-piece-controls" hidden>',
            '<button type="button" class="lo-drill-piece-prev">← Previous idea</button>',
            '<span class="lo-drill-piece-count" aria-live="polite"></span>',
            '<button type="button" class="lo-drill-piece-next">Next idea →</button>',
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
        partsBtn = $(".lo-drill-parts"), subpartsBtn = $(".lo-drill-subparts"),
        detailsBtn = $(".lo-drill-details"),
        partBar = $(".lo-drill-part-controls"),
        subpartBar = $(".lo-drill-subpart-controls"), pieceBar = $(".lo-drill-piece-controls"),
        prevSubpart = $(".lo-drill-subpart-prev"), nextSubpart = $(".lo-drill-subpart-next"),
        prevPiece = $(".lo-drill-piece-prev"), nextPiece = $(".lo-drill-piece-next"),
        prevPart = $(".lo-drill-part-prev"), nextPart = $(".lo-drill-part-next"),
        prev = $(".lo-drill-prev"), next = $(".lo-drill-next"),
        counter = $(".lo-drill-count"), partCounter = $(".lo-drill-part-count"),
        subpartCounter = $(".lo-drill-subpart-count"),
        pieceCounter = $(".lo-drill-piece-count"),
        scroller = $(".lo-drill-scroll"), close = $(".lo-drill-close");
      $(".lo-drill-context").textContent = course + " · " + strand;
      let position = 0, part = 0, subpart = 0, piece = 0, mode = "whole", trigger = null;
      function hierarchy(outcome) {
        const items = outcome.statements;
        const hasLead = items.length > 0 && /(:|so that they can)\s*$/i.test(text(items[0]));
        const lead = hasLead ? items[0] : null;
        const groups = [];
        let current = null, roman = null;
        for (const p of (hasLead ? items.slice(1) : items)) {
          const value = text(p);
          // Main alphabetic parts appear as a), b), c), etc.
          const letter = value.match(/^([a-z])\)\s*/i) ||
                         value.match(/^([a-hj-uw-z])\.\s+/i);
          const numeral = value.match(/^(viii|vii|vi|iv|iii|ii|ix|v|i|x)\.\s+/i);
          if (letter) {
            current = {label:letter[1].toLowerCase(), nodes:[p], roman:[]};
            groups.push(current);
            roman = null;
          } else if (numeral && current?.label) {
            roman = {label:numeral[1].toLowerCase(), nodes:[p]};
            current.roman.push(roman);
          } else if (roman) {
            // Continuation of roman statement, e.g. the five index laws in N.1(c)(iii).
            roman.nodes.push(p);
          } else if (current?.label) {
            current.nodes.push(p);
          } else {
            current = {label:"",nodes:[p],roman:[]};
            groups.push(current);
          }
        }
        return {lead, groups};
      }
      function appendClones(target, nodes) {
        target.replaceChildren(...nodes.map(safeClone));
      }
      function romanPieces(roman) {
        if (!roman) return {lead:null,items:[]};
        const hasLead = roman.nodes.length > 1 && /:\s*$/.test(text(roman.nodes[0]));
        if (hasLead) return {lead:roman.nodes[0], items:roman.nodes.slice(1)};
        if (roman.nodes.length === 1) return {lead:null,items:detailPieces(roman.nodes[0])};
        return {lead:null,items:roman.nodes.flatMap(detailPieces)};
      }
      function activeContext() {
        const outline=hierarchy(outcomes[position]);
        if (part>=outline.groups.length) part=0;
        const group=outline.groups[part];
        if (subpart >= (group?.roman.length || 1)) subpart=0;
        const roman=group?.roman[subpart];
        const eq=roman ? romanPieces(roman) : {lead:null,items:group?.nodes.flatMap(detailPieces) || []};
        if (piece>=Math.max(eq.items.length,1)) piece=0;
        return {outline, group, roman, eq};
      }
      function preferredMode(outcome, group, roman) {
        if (roman) {
          const rp=romanPieces(roman);
          if (rp.items.length > 1) return "details";
          return "subparts";
        }
        return hierarchy(outcome).groups.length>1 ? "parts" : "whole";
      }
      function render() {
        const {outline,group,roman,eq}=activeContext();
        if (!group) {mode="whole";}
        if (mode==="subparts" && !roman) mode="parts";
        if (mode==="details" && eq.items.length<2) mode=roman?"subparts":"parts";
        const outcome=outcomes[position];
        title.textContent=outcome.code+(outcome.heading?" — "+outcome.heading:"");
        counter.textContent=(position+1)+" of "+outcomes.length;
        prev.disabled=position===0;next.disabled=position===outcomes.length-1;
        const partAvailable=outline.groups.length>1;
        partsBtn.hidden=!partAvailable;
        subpartsBtn.hidden=!(group?.roman.length);
        detailsBtn.hidden=eq.items.length<2;
        $(".lo-drill-mode").hidden=!partAvailable && !(group?.roman.length) && eq.items.length<2;
        wholeBtn.setAttribute("aria-pressed",String(mode==="whole"));
        partsBtn.setAttribute("aria-pressed",String(mode==="parts"));
        subpartsBtn.setAttribute("aria-pressed",String(mode==="subparts"));
        detailsBtn.setAttribute("aria-pressed",String(mode==="details"));
        intro.replaceChildren();
        partBar.hidden=mode!=="parts" || !partAvailable;
        subpartBar.hidden=mode!=="subparts" || !roman;
        pieceBar.hidden=mode!=="details" || eq.items.length<2;
        if (mode==="whole") {
          appendClones(content,outcome.statements);
        } else if (mode==="parts") {
          if(outline.lead) appendClones(intro,[outline.lead]);
          appendClones(content,[...group.nodes,...group.roman.flatMap(entry=>entry.nodes)]);
        } else if (mode==="subparts" && roman) {
          appendClones(intro,[...(outline.lead?[outline.lead]:[]),...group.nodes]);
          appendClones(content,roman.nodes);
        } else if (mode==="details") {
          const leadNodes=[
            ...(outline.lead?[outline.lead]:[]),
            ...(roman?group.nodes:[]),
            ...(eq.lead?[eq.lead]:[])
          ];
          appendClones(intro,leadNodes);
          appendClones(content,eq.items[piece]?[eq.items[piece]]:[]);
          pieceCounter.textContent="Equation / idea "+(piece+1)+" of "+eq.items.length;
          prevPiece.disabled=piece===0;
          nextPiece.disabled=piece===eq.items.length-1;
        }
        if (partAvailable) {
          partCounter.textContent=(group.label?group.label+") · ":"")+"Part "+(part+1)+" of "+outline.groups.length;
          prevPart.disabled=part===0;
          nextPart.disabled=part===outline.groups.length-1;
        }
        if (roman) {
          subpartCounter.textContent=roman.label.toUpperCase()+". · Subpart "+(subpart+1)+" of "+group.roman.length;
          prevSubpart.disabled=subpart===0;
          nextSubpart.disabled=subpart===group.roman.length-1;
        }
        scroller.scrollTop=0;
        if(window.MathJax?.typesetPromise && !content.querySelector("mjx-container"))
          window.MathJax.typesetPromise([content,intro]).catch(()=>{});
      }
      function changePart(offset) {
        const outline=hierarchy(outcomes[position]);
        const target=part+offset;
        if(target<0||target>=outline.groups.length)return;
        part=target;subpart=0;piece=0;
        mode=preferredMode(outcomes[position],outline.groups[part],null);
        // For a deep branch, show one roman subpart rather than all its formulas.
        if(outline.groups[part].roman.length) mode="subparts";
        render();
      }
      function changeSubpart(offset) {
        const outline=hierarchy(outcomes[position]),group=outline.groups[part];
        const target=subpart+offset;
        if(!group||target<0||target>=group.roman.length)return;
        subpart=target;piece=0;
        mode=preferredMode(outcomes[position],group,group.roman[subpart]);
        render();
      }
      function changeOutcome(offset) {
        const target=position+offset;
        if(target<0||target>=outcomes.length)return;
        position=target;part=0;subpart=0;piece=0;
        const outline=hierarchy(outcomes[position]);
        mode=preferredMode(outcomes[position],outline.groups[0],null);
        render();
      }
      outcomes.forEach((outcome,i)=>{
        const open=document.createElement("button");
        open.type="button";open.className="lo-drill-open";
        open.textContent="Enlarge "+outcome.code;
        open.setAttribute("aria-label","Read learning outcome "+outcome.code);
        open.addEventListener("click",()=>{
          trigger=open;position=i;part=0;subpart=0;piece=0;
          const outline=hierarchy(outcomes[position]);
          mode=preferredMode(outcomes[position],outline.groups[0],null);
          render();dialog.showModal();close.focus();
        });
        outcome.labelCell.appendChild(open);
        outcome.statementCell.classList.add("lo-drill-clickable");
        outcome.statementCell.addEventListener("click",event=>{
          if(event.target.closest("a,button")||window.getSelection()?.toString())return;
          open.click();
        });
      });
      wholeBtn.addEventListener("click",()=>{mode="whole";piece=0;render();});
      partsBtn.addEventListener("click",()=>{mode="parts";piece=0;render();});
      subpartsBtn.addEventListener("click",()=>{mode="subparts";piece=0;render();});
      detailsBtn.addEventListener("click",()=>{mode="details";piece=0;render();});
      prevPart.addEventListener("click",()=>changePart(-1));
      nextPart.addEventListener("click",()=>changePart(1));
      prevSubpart.addEventListener("click",()=>changeSubpart(-1));
      nextSubpart.addEventListener("click",()=>changeSubpart(1));
      prevPiece.addEventListener("click",()=>{if(piece>0){piece--;render();}});
      nextPiece.addEventListener("click",()=>{
        const total=activeContext().eq.items.length;
        if(piece<total-1){piece++;render();}
      });
      prev.addEventListener("click",()=>changeOutcome(-1));
      next.addEventListener("click",()=>changeOutcome(1));
      close.addEventListener("click",()=>dialog.close());
      dialog.addEventListener("close",()=>{if(trigger?.isConnected)trigger.focus();});
      dialog.addEventListener("keydown",event=>{
        if(event.ctrlKey||event.altKey||event.metaKey||event.target instanceof HTMLInputElement)return;
        if(event.key!=="ArrowLeft"&&event.key!=="ArrowRight")return;
        event.preventDefault();
        const direction=event.key==="ArrowRight"?1:-1;
        if(event.shiftKey)changeOutcome(direction);
        else if(mode==="details"){
          const ctx=activeContext(),target=piece+direction;
          if(target>=0&&target<ctx.eq.items.length){piece=target;render();}
          else if(ctx.roman)changeSubpart(direction);
          else changePart(direction);
        }else if(mode==="subparts")changeSubpart(direction);
        else if(mode==="parts")changePart(direction);
        else changeOutcome(direction);
      });
    }
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", install, {once:true});
  else install();
})();