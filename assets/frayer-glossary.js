/* Frayer Diagram Glossary — progressive enhancement of native PreTeXt glossary.
   Definitions remain in shared-glossary.ptx and are read from the published page. */
(() => {
  "use strict";
  const data = {
    "absolute-value":["The absolute value is never negative. On the real number line it also measures distance from zero.","|−5| = 5; |3| = 3; |0| = 0","|−5| is not −5"],
    "algebraic-expression":["Variables, constants and operations; no equality assertion.","3x + 7; 2(a − b)","3x + 7 = 16 is an equation"],
    "algorithm":["Finite, precisely specified steps for a task.","Long division; Euclidean algorithm","'Try some numbers' is not a precise algorithm"],
    "area":["Area measures a region, not its boundary; units are squared.","Rectangle 3 cm by 4 cm: 12 cm²","12 cm is a length, not an area"],
    "bracket":["Groups operations and expressions; can change order of calculation.","3(x + 2); (a − b)²","3x + 2 has no grouping bracket"],
    "coefficient":["A coefficient can be numerical or symbolic, and may be negative.","7x has coefficient 7; −y has coefficient −1; ax has coefficient a","In x + 7, the coefficient of x is 1, not 7"],
    "conceptual-understanding":["Explains meaning and why a method works.","Explaining why a(b+c)=ab+ac","Reciting the rule without knowing why"],
    "constant":["Value fixed within the context; may depend on the model.","The 5 in 3x + 5","x in 3x + 5 when x may vary"],
    "counterexample":["One valid case that disproves a universal claim.","2 disproves 'all primes are odd'","An example supporting the claim"],
    "degree":["For a multivariable term, add the variable exponents; the zero polynomial is a special case.","3x² + x has degree 2; x²y³ has total degree 5","1/x is not a polynomial; the highest single exponent is not always the total degree"],
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
    "linear-expression":["No products of variables or powers above one; at least one variable term is present. A constant term is allowed. In strict linear algebra, a non-zero constant term makes the expression affine.","3x+2; 2x−5y+7; −4a+b","x²+3; xy+2; 1/x+4"],
    "mathematical-model":["Uses mathematics to represent and analyse reality.","Distance = speed × time at constant speed","An unsupported guess without a representation"],
    "principle":["Underlying mathematical justification.","Distribution justifies expanding brackets","A remembered trick without justification"],
    "mean":["For n numerical observations, add all n values and divide by n, with n>0.","Mean of 2,4,9 is 5","The middle value is the median, not necessarily the mean"],
    "median":["Middle value after ordering; average two central values if even.","Median of 2,7,8 is 7","Largest value is not necessarily median"],
    "mode":["A data set may have two or more most-frequent values. The mode is not necessarily the mean.","Mode of 1,2,2,3 is 2; the modes of 1,1,2,2 are 1 and 2","For 1,1,1,9, the mean is 3, but the mode is 1"],
    "numerator":["Part of a fraction above the bar.","3 in 3/5","5 is the denominator of 3/5"],
    "outcome":["One possible result of a trial.","Rolling a 4 on a die","{2,4,6} is an event with multiple outcomes"],
    "parameter":["Fixed in one model, variable across models.","m in y=mx+c when selecting a line","x is the input variable in y=mx+c"],
    "polynomial":["No negative or fractional exponents on variables; coefficients may be real numbers or parameters.","3x²−2x+7; 2xy²+5","1/x and √x are not polynomials in x"],
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



  // One click, one popup. The definition is sourced from native PreTeXt,
  // not duplicated in the JavaScript data table.
  const dialog = document.createElement("dialog");
  dialog.className = "frayer-dialog";
  dialog.setAttribute("aria-label","Mathematical glossary");
  dialog.innerHTML = '<div class="frayer-inner"><div class="frayer-top"><span>MATHEMATICAL GLOSSARY</span><button class="frayer-close" type="button" aria-label="Close definition">×</button></div><h2 class="frayer-title"></h2><div class="frayer-definition"><h3>Definition</h3><div class="frayer-definition-content"></div></div><div class="frayer-grid"><section class="frayer-cell"><h3>Characteristics</h3><p></p></section><section class="frayer-cell"><h3>Examples</h3><p></p></section><section class="frayer-cell"><h3>Non-examples</h3><p></p></section></div></div>';
  document.body.append(dialog);
  const closeButton = dialog.querySelector(".frayer-close");
  let lastTrigger = null;
  closeButton.addEventListener("click",()=>dialog.close());
  dialog.addEventListener("click",e=>{if(e.target===dialog)dialog.close();});
  dialog.addEventListener("close",()=>{if(lastTrigger?.isConnected)lastTrigger.focus({preventScroll:true});});

  function locateEntry(doc,slug) {
    const element=doc.getElementById("glossary-"+slug);
    if(!element)return null;
    const dt=element.closest("dt") || (element.matches("dt")?element:null);
    const root=dt || element.closest(".glossary-item, .gi, li") || element;
    let paragraph;
    if(dt) {
      const dd=dt.nextElementSibling;
      paragraph=dd?.matches("dd") ? (dd.querySelector("p") || dd) : dt.querySelector("p");
    } else {
      paragraph=root.querySelector("dd p, .description p, p, dd") || null;
      if(!paragraph && root.nextElementSibling?.matches("dd"))
        paragraph=root.nextElementSibling.querySelector("p") || root.nextElementSibling;
    }
    if(!paragraph)return null;
    const heading=dt || root.querySelector(".heading .title, .title, dt, h3, h4, strong, b");
    const title=(heading?.textContent || slug.replace(/-/g," ")).trim().replace(/\.$/,"");
    return {title, paragraph, heading};
  }

  let remoteGlossary=null;
  async function getEntry(slug) {
    const onPage=locateEntry(document,slug);
    if(onPage)return onPage;
    if(!remoteGlossary)remoteGlossary=fetch("chapter-glossary.html",{credentials:"same-origin"})
      .then(response=>{if(!response.ok)throw Error("Glossary unavailable");return response.text();})
      .then(html=>new DOMParser().parseFromString(html,"text/html"))
      .catch(error=>{remoteGlossary=null;throw error;});
    return locateEntry(await remoteGlossary,slug);
  }
  function showPopup(slug,entry,trigger) {
    const panels=data[slug];
    if(!panels)return;
    lastTrigger=trigger || document.activeElement;
    dialog.querySelector(".frayer-title").textContent=entry.title;
    const definition=dialog.querySelector(".frayer-definition-content");
    definition.replaceChildren(entry.paragraph.cloneNode(true));
    dialog.querySelectorAll(".frayer-cell p").forEach((p,i)=>{p.textContent=panels[i];});
    if(!dialog.open)dialog.showModal();
    if(!definition.querySelector("mjx-container") && window.MathJax?.typesetPromise)
      window.MathJax.typesetPromise([definition]).catch(()=>{});
    closeButton.focus();
  }
  async function openTerm(slug,trigger,fallbackUrl) {
    if(!Object.hasOwn(data,slug))return;
    try {
      const entry=await getEntry(slug);
      if(!entry)throw Error("Definition not found: "+slug);
      showPopup(slug,entry,trigger);
    }catch(error) {
      console.warn("Glossary pop-up unavailable",error);
      if(fallbackUrl)window.location.assign(fallbackUrl);
    }
  }

  // The alphabetic list retains its concise definitions. Click the term for
  // a single richer pop-up. No secondary controls or jargon in the interface.
  let mounted=0;
  for(const slug of Object.keys(data)) {
    const entry=locateEntry(document,slug);
    if(!entry)continue;
    const heading=entry.heading;
    if(!heading)continue;
    heading.classList.add("frayer-clickable-title");
    heading.setAttribute("role","button");
    heading.setAttribute("tabindex","0");
    heading.setAttribute("aria-label","Read more about "+entry.title);
    heading.addEventListener("click",e=>{
      e.preventDefault();
      e.stopPropagation();
      openTerm(slug,heading);
    });
    heading.addEventListener("keydown",e=>{
      if(e.key==="Enter"||e.key===" "){e.preventDefault();openTerm(slug,heading);}
    });
    mounted++;
  }

  // Links to definitions from chapters also open in place, without changing page.
  document.addEventListener("click",e=>{
    const link=e.target.closest("a[href]");
    if(!link || link.closest("dialog"))return;
    const url=new URL(link.href,document.baseURI);
    if(url.origin!==location.origin || !url.pathname.endsWith("/chapter-glossary.html"))return;
    const match=url.hash.match(/^#glossary-([a-z0-9-]+)$/i);
    if(!match || !Object.hasOwn(data,match[1]))return;
    e.preventDefault();
    openTerm(match[1],link,url.href);
  });
  // Only explicitly marked terminology, not incidental words, becomes clickable.
  const titleToSlug=new Map(Object.keys(data).map(slug=>[slug.replace(/-/g," "),slug]));
  document.querySelectorAll("em.terminology, span.terminology, em.term, span.term").forEach(node=>{
    if(node.closest("a, button, dialog, .glossary, .frayer-dialog"))return;
    const title=node.textContent.trim().toLowerCase().replace(/[.,;:]+$/,"");
    const slug=titleToSlug.get(title);
    if(!slug)return;
    node.classList.add("glossary-term-inline");
    node.tabIndex=0;
    node.setAttribute("role","button");
    node.setAttribute("aria-label","Read more about "+title);
    node.addEventListener("click",()=>openTerm(slug,node));
    node.addEventListener("keydown",e=>{
      if(e.key==="Enter"||e.key===" "){e.preventDefault();openTerm(slug,node);}
    });
  });
  document.documentElement.dataset.frayerMounted=String(mounted);
})();
