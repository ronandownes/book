/* Frayer Diagram Glossary — progressive enhancement of native PreTeXt glossary.
   Definitions remain in shared-glossary.ptx and are read from the published page. */
(() => {
  "use strict";
  const data = {
    "absolute-value":["Distance from zero; never negative.","|−5| = 5; |3| = 3","−5 is not the absolute value of −5"],
    "algebraic-expression":["Variables, constants and operations; no equality assertion.","3x + 7; 2(a − b)","3x + 7 = 16 is an equation"],
    "algorithm":["Finite, precisely specified steps for a task.","Long division; Euclidean algorithm","'Try some numbers' is not a precise algorithm"],
    "area":["Two-dimensional measure; square units.","Rectangle 3 cm by 4 cm: 12 cm²","12 cm is a length, not an area"],
    "bracket":["Groups operations and expressions; can change order of calculation.","3(x + 2); (a − b)²","3x + 2 has no grouping bracket"],
    "coefficient":["Multiplier attached to a variable term.","7x has coefficient 7; −y has coefficient −1","7 is a constant term in x + 7"],
    "conceptual-understanding":["Explains meaning and why a method works.","Explaining why a(b+c)=ab+ac","Reciting the rule without knowing why"],
    "constant":["Value fixed within the context; may depend on the model.","The 5 in 3x + 5","x in 3x + 5 when x may vary"],
    "counterexample":["One valid case that disproves a universal claim.","2 disproves 'all primes are odd'","An example supporting the claim"],
    "degree":["Highest total degree of a non-zero polynomial term.","3x² + x has degree 2","1/x is not a polynomial"],
    "denominator":["Divisor below the fraction bar; cannot equal zero.","3/5: denominator 5","3 is the numerator in 3/5"],
    "distributive-law":["Multiplication applied to each term of a sum.","2(x + 3) = 2x + 6","2(x + 3) = 2x + 3"],
    "equation":["Statement asserting equality of two expressions.","2x + 1 = 7","2x + 1 alone is an expression"],
    "equivalence":["Identical values on their shared permitted domain.","2(x+1) and 2x+2","x+1 and x+2"],
    "estimate":["Reasoned approximation, not necessarily exact.","49 × 21 is about 1,000","An exact result without approximation"],
    "event":["Subset of a sample space.","Even die outcomes {2,4,6}","An outcome of 8 on a six-sided die"],
    "expand":["Uses distribution to rewrite a product.","3(x+2) → 3x+6","3x+6 → 3(x+2) is factorising"],
    "expression":["Represents a mathematical value; asserts no relation.","x² + 1; 4/5","x² + 1 = 5 is an equation"],
    "factor":["A quantity in a multiplication.","2 and 3 are factors of 6","2 and 3 in 2+3 are addends"],
    "factorisation":["Expressing a quantity as a product.","x²−9 = (x−3)(x+3)","(x+2)(x+3) → x²+5x+6 expands"],
    "function":["Each allowed input has exactly one output.","f(x)=x², with specified domain","One input mapped to two distinct outputs"],
    "generalisation":["Claim extending beyond observed examples.","The sum of two even integers is even","Only checking 2+4=6"],
    "heuristic":["Useful strategy, not a guaranteed algorithm.","Draw a diagram; try a simpler case","A fully prescribed guaranteed procedure"],
    "identity":["True for every permitted value.","(x+1)²=x²+2x+1","x+1=4 only when x=3"],
    "inequality":["Compares values with an order relation.","x < 5; 2 ≥ −1","x = 5 is equality"],
    "intersection":["Elements shared by the sets.","{1,2} ∩ {2,3} = {2}","{1,2} ∪ {2,3} = {1,2,3}"],
    "like-terms":["Same variable factors with identical exponents.","3x² and −7x²","3x and 3x²"],
    "linear-expression":["First-degree non-constant polynomial; each term has total degree at most one. In school usage a constant term may be included.","3x+2; 2x−5y+7; −4a+b","x²+3; xy+2; 1/x+4"],
    "mathematical-model":["Uses mathematics to represent and analyse reality.","Distance = speed × time at constant speed","An unsupported guess without a representation"],
    "principle":["Underlying mathematical justification.","Distribution justifies expanding brackets","A remembered trick without justification"],
    "mean":["Sum divided by the number of observations.","Mean of 2,4,9 is 5","The middle value is the median"],
    "median":["Middle value after ordering; average two central values if even.","Median of 2,7,8 is 7","Largest value is not necessarily median"],
    "mode":["Most frequent observed value or category.","Mode of 1,2,2,3 is 2","Mean of 1,2,2,3 is 2, but means differ in general"],
    "numerator":["Part of a fraction above the bar.","3 in 3/5","5 is the denominator of 3/5"],
    "outcome":["One possible result of a trial.","Rolling a 4 on a die","{2,4,6} is an event with multiple outcomes"],
    "parameter":["Fixed in one model, variable across models.","m in y=mx+c when selecting a line","x is the input variable in y=mx+c"],
    "polynomial":["Sum of monomials with non-negative integer variable powers.","3x²−2x+7","1/x and √x are not polynomials"],
    "probability":["Between 0 and 1 inclusive; measures likelihood.","P(heads)=1/2 for a fair coin","A probability of 1.4"],
    "procedural-fluency":["Accurate, flexible, efficient method selection and execution.","Choosing mental arithmetic for 25×4","Knowing a single routine but unable to adapt"],
    "procedure":["Ordered actions to complete a task.","Steps to solve a linear equation","An unstructured guess"],
    "proof":["Logical argument covering every case under assumptions.","Proving even + even is even","Testing 100 examples alone"],
    "representation":["Mathematical idea shown in varied forms.","A graph, table, equation or Venn diagram","A diagram unrelated to the stated quantities"],
    "sample-space":["Set of all possible outcomes.","Fair coin: {H,T}","{H} alone omits a possible result"],
    "simplify":["Equivalent rewriting suited to a purpose.","2x+3x → 5x","2x+3x → 6x changes its value"],
    "solution-set":["Every value satisfying a stated relation and domain.","x²=4 over R: {−2,2}","{2} omits −2 over the reals"],
    "strategic-competence":["Formulate, represent, choose and solve.","Trying a table then a general rule","Applying a formula without interpreting the question"],
    "surface-area":["Combined outside area of a solid; square units.","Cube side 2 cm: 24 cm²","Cube volume is 8 cm³"],
    "term":["Additive part of an expression, including its sign.","3x and −5 in 3x−5","3 and x are factors within 3x"],
    "union":["Every element in either set, counted once.","{1,2} ∪ {2,3} = {1,2,3}","{2} is the intersection, not the union"],
    "variable":["Symbol for an unknown or changing quantity.","x in y=2x+3","The 3 is a constant term"],
    "volume":["Three-dimensional space occupied; cubic units.","Cuboid 2×3×4 cm: 24 cm³","24 cm² describes an area"]
  };


  // Progressive disclosure: a quick glossary definition comes before the
  // optional Frayer view. The PreTeXt glossary is the only canonical definition.
  const summary = document.createElement("dialog");
  summary.className = "glossary-quick-dialog";
  summary.setAttribute("aria-label", "Glossary definition");
  summary.innerHTML = '<div class="glossary-quick-inner"><div class="glossary-quick-top"><span>MATHEMATICAL GLOSSARY</span><button class="glossary-quick-close" type="button" aria-label="Close definition">×</button></div><h2 class="glossary-quick-title"></h2><div class="glossary-quick-definition"></div><div class="glossary-quick-actions"><button class="glossary-quick-explore" type="button">Explore Frayer diagram</button><button class="glossary-quick-done" type="button">That's enough</button></div></div>';
  document.body.append(summary);
  const frayer = document.createElement("dialog");
  frayer.className = "frayer-dialog";
  frayer.setAttribute("aria-label", "Frayer diagram");
  frayer.innerHTML = '<div class="frayer-inner"><div class="frayer-top"><span>EXPLORE THE CONCEPT · FRAYER DIAGRAM</span><button class="frayer-close" type="button" aria-label="Close Frayer diagram">×</button></div><h2 class="frayer-title"></h2><div class="frayer-definition"><h3>Definition</h3><div class="frayer-definition-content"></div></div><div class="frayer-grid"><section class="frayer-cell"><h3>Characteristics</h3><p></p></section><section class="frayer-cell"><h3>Examples</h3><p></p></section><section class="frayer-cell"><h3>Non-examples</h3><p></p></section></div><div class="frayer-footer"><button class="frayer-back" type="button">← Back to definition</button></div><p class="frayer-note">What do the examples have in common? Why do the non-examples not qualify?</p></div>';
  document.body.append(frayer);

  let active = null;
  let lastTrigger = null;
  const quickClose = summary.querySelector(".glossary-quick-close");
  const frayerClose = frayer.querySelector(".frayer-close");
  const closeSummary = () => summary.close();
  quickClose.addEventListener("click", closeSummary);
  summary.querySelector(".glossary-quick-done").addEventListener("click", closeSummary);
  summary.addEventListener("click",e=>{if(e.target===summary)closeSummary();});
  frayerClose.addEventListener("click",()=>frayer.close());
  frayer.addEventListener("click",e=>{if(e.target===frayer)frayer.close();});
  summary.addEventListener("close",()=>{if(!frayer.open&&lastTrigger?.isConnected)lastTrigger.focus({preventScroll:true});});
  frayer.addEventListener("close",()=>{if(!summary.open&&lastTrigger?.isConnected)lastTrigger.focus({preventScroll:true});});

  const titles = new Map();
  function extractDefinition(root) {
    if (!root) return null;
    // PreTeXt output may put the xml:id on an entry wrapper or on <dt>.
    if (root.matches("p")) return root;
    const inside = root.querySelector("dd p, p, dd, .description");
    if (inside) return inside;
    if (root.matches("dt")) {
      const dd = root.nextElementSibling;
      if (dd?.matches("dd")) return dd.querySelector("p") || dd;
    }
    const next = root.nextElementSibling;
    if (next?.matches("dd")) return next.querySelector("p") || next;
    return null;
  }
  function entryTitle(root,slug) {
    if (!root) return slug.replace(/-/g," ");
    const heading = root.matches("dt")?root:root.querySelector(".heading .title, dt, .title, h3, h4, strong, b");
    return (heading?.textContent||slug.replace(/-/g," ")).trim().replace(/\.$/,"");
  }
  function entryInDocument(doc,slug) {
    const node = doc.getElementById("glossary-"+slug);
    if (!node) return null;
    const root = extractDefinition(node) ? node : (node.closest("dt, dd, li.glossary-item, .glossary-item, .gi") || node.parentElement);
    const paragraph = extractDefinition(root);
    return paragraph ? {title:entryTitle(root,slug),paragraph} : null;
  }
  let glossaryLoad = null;
  async function getEntry(slug) {
    const local = entryInDocument(document,slug);
    if (local) return local;
    if (!glossaryLoad) {
      glossaryLoad = fetch("chapter-glossary.html", {credentials:"same-origin"})
        .then(r=>{if(!r.ok)throw new Error("Glossary unavailable");return r.text();})
        .then(html=>new DOMParser().parseFromString(html,"text/html"))
        .catch(e=>{glossaryLoad=null;throw e;});
    }
    return entryInDocument(await glossaryLoad,slug);
  }
  function typesetMath(element) {
    if (!element.querySelector("mjx-container") && window.MathJax?.typesetPromise) window.MathJax.typesetPromise([element]).catch(()=>{});
  }
  function copyDefinition(node) {
    const clone=node.cloneNode(true);
    // Render the source's math anew rather than copying MathJax layout artefacts.
    // Retain already-rendered maths when copying from the source page.
    return clone;
  }
  function showDefinition(slug,entry,trigger) {
    active={slug,entry};
    lastTrigger=trigger||document.activeElement;
    summary.querySelector(".glossary-quick-title").textContent=entry.title;
    const box=summary.querySelector(".glossary-quick-definition");
    box.replaceChildren(copyDefinition(entry.paragraph));
    if (frayer.open) frayer.close();
    if (!summary.open) summary.showModal();
    typesetMath(box);
    quickClose.focus();
  }
  function showFrayer() {
    if (!active) return;
    const {slug,entry}=active;
    const panels=data[slug];
    if (!panels) return;
    if (summary.open) summary.close();
    frayer.querySelector(".frayer-title").textContent=entry.title;
    const box=frayer.querySelector(".frayer-definition-content");
    box.replaceChildren(copyDefinition(entry.paragraph));
    frayer.querySelectorAll(".frayer-cell p").forEach((p,i)=>{p.textContent=panels[i];});
    if(!frayer.open)frayer.showModal();
    typesetMath(box);
    frayerClose.focus();
  }
  summary.querySelector(".glossary-quick-explore").addEventListener("click",showFrayer);
  frayer.querySelector(".frayer-back").addEventListener("click",()=>{
    if(!active)return;
    frayer.close();
    showDefinition(active.slug,active.entry,lastTrigger);
  });
  async function start(slug,trigger,fallbackHref) {
    if (!Object.hasOwn(data,slug)) return;
    try {
      const entry=await getEntry(slug);
      if (!entry) throw new Error("No glossary definition for "+slug);
      showDefinition(slug,entry,trigger);
    } catch (e) {
      console.warn("Glossary definition could not open",e);
      if(fallbackHref) window.location.assign(fallbackHref);
    }
  }
  let mounted=0;
  // Keep the complete alphabetical glossary readable. Clicking a term opens
  // its *definition*, and only the separate button opens a Frayer diagram.
  for(const slug of Object.keys(data)) {
    const node=document.getElementById("glossary-"+slug);
    if(!node)continue;
    const root=extractDefinition(node) ? node : (node.closest("dt, dd, li.glossary-item, .glossary-item, .gi") || node.parentElement);
    const paragraph=extractDefinition(root);
    if(!paragraph)continue;
    root.classList.add("frayer-entry");
    const heading=root.matches("dt")?root:root.querySelector(".heading .title, dt, .title, h3, h4, strong, b");
    const button=document.createElement("button");
    button.type="button";
    button.className="frayer-trigger";
    button.textContent="Explore Frayer diagram";
    button.setAttribute("aria-label","Explore Frayer diagram for "+entryTitle(root,slug));
    button.addEventListener("click",()=>{
      const entry=entryInDocument(document,slug);
      if(!entry)return;
      active={slug,entry};
      lastTrigger=button;
      showFrayer();
    });
    paragraph.insertAdjacentElement("afterend",button);
    if(heading&&!heading.closest("a")) {
      heading.classList.add("frayer-clickable-title");
      heading.tabIndex=0;
      heading.setAttribute("role","button");
      heading.setAttribute("aria-label","Read glossary definition for "+entryTitle(root,slug));
      heading.addEventListener("click",e=>{if(!e.target.closest("a"))start(slug,heading);});
      heading.addEventListener("keydown",e=>{
        if(e.key==="Enter"||e.key===" "){e.preventDefault();start(slug,heading);}
      });
    }
    mounted++;
  }
  // Where textbook hyperlinks already point to glossary entries, offer
  // an in-page definition first, with ordinary navigation as a fallback.
  document.addEventListener("click",e=>{
    const a=e.target.closest("a[href]");
    if(!a)return;
    const url=new URL(a.href,document.baseURI);
    if(url.origin!==window.location.origin || !url.pathname.endsWith("/chapter-glossary.html"))return;
    const match=url.hash.match(/^#glossary-([a-z0-9-]+)$/i);
    if(!match || !Object.hasOwn(data,match[1]))return;
    e.preventDefault();
    start(match[1],a,url.href);
  });
  // Explicitly marked PreTeXt terminology can also open the quick glossary.
  // Only exact known terms are enhanced; arbitrary words remain untouched.
  const byTitle=new Map(Object.keys(data).map(slug=>[slug.replace(/-/g," "),slug]));
  document.querySelectorAll("em.terminology, span.terminology, em.term, span.term").forEach(node=>{
    if(node.closest("a, button, dialog, .frayer-entry"))return;
    const name=node.textContent.trim().toLowerCase().replace(/[.,;:]+$/,"");
    const slug=byTitle.get(name);
    if(!slug)return;
    node.classList.add("glossary-term-inline");
    node.tabIndex=0;
    node.setAttribute("role","button");
    node.setAttribute("aria-label","Read glossary definition for "+name);
    node.addEventListener("click",()=>start(slug,node));
    node.addEventListener("keydown",e=>{
      if(e.key==="Enter"||e.key===" "){e.preventDefault();start(slug,node);}
    });
  });
  document.documentElement.dataset.frayerMounted=String(mounted);
})();
