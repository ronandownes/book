/* Frayer Diagram Glossary — progressive enhancement of native PreTeXt glossary.
   Definitions remain in shared-glossary.ptx and are read from the published page. */
(() => {
  "use strict";
  const data = {
    "absolute-value":["The absolute value is never negative. On the real number line it also measures distance from zero.",["|−4| = 4","|3| = 3","|0| = 0","|4 − 9| = 5"],["|−4| = −4 (incorrect)","|3| = −3 (incorrect)","|0| = 1 (incorrect)"]],
    "algebraic-expression":["Variables, constants and operations; no equality assertion.",["3x + 7","(x − 2)(x + 5)","a² + b²"],["3x + 7 = 16 (equation)","x > 3 (inequality)","x ∈ A (membership statement)"]],
    "algorithm":["Finite, precisely specified steps for a task.",["Long division","Euclidean algorithm for HCF","Binary search of a sorted list"],["'Try something' without defined steps","An unstructured guess","A sketch alone, without a procedure"]],
    "area":["Area measures a region, not its boundary; units are squared.",["Rectangle 4 cm × 3 cm: 12 cm²","Triangle, base 6 cm and height 4 cm: 12 cm²","Circle of radius 2 cm: 4π cm²","Irregular region estimated using Simpson’s rule"],["Perimeter of the rectangle: 14 cm","Circumference of the circle: 4π cm","Volume of a 2 × 3 × 4 cm cuboid: 24 cm³"]],
    "bracket":["Groups operations and expressions; can change order of calculation.",["3(x + 2)","(−2)²","[a + (b − c)]"],["3x + 2 has no grouping brackets","The multiplication symbol × is not a bracket","The equals sign = is not a bracket"]],
    "coefficient":["A coefficient can be numerical or symbolic, and may be negative.",["7x: coefficient 7","−y: coefficient −1","ax: coefficient a","3x²: coefficient 3"],["The 7 in x + 7 is a constant term","The 2 in x² is an exponent","The x in 5x is the variable, not its numerical coefficient"]],
    "conceptual-understanding":["Explains meaning and why a method works.",["Explaining why a(b + c) = ab + ac","Showing that 1/2 = 2/4 using a diagram","Explaining why x = x¹"],["Memorising the formula without meaning","Blind substitution into an unsuitable formula","Repeating steps without understanding them"]],
    "constant":["Value fixed within the context; may depend on the model.",["5 in 3x + 5","π as a fixed mathematical value","c in a chosen line y = mx + c"],["x in 3x + 5 when x varies","t as elapsed time","n as a changing counting index"]],
    "counterexample":["One valid case that disproves a universal claim.",["2 disproves 'every prime is odd'","−3 disproves 'all integers are positive'","A scalene triangle disproves 'every triangle is equilateral'"],["Another odd prime does not disprove the first claim","One supporting example is not a counterexample","An unrelated observation cannot disprove the claim"]],
    "degree":["For a multivariable term, add the variable exponents; the zero polynomial is a special case.",["x⁴ + 1 has degree 4","2x²y³ has total degree 5","Non-zero constant 7 has degree 0"],["1/x is not a polynomial","√x is not a polynomial in x","Calling x²y³ degree 3 ignores the total degree"]],
    "denominator":["Divisor below the fraction bar; cannot equal zero.",["3/5: denominator 5","(x + 1)/(x − 2): denominator x − 2","1/x: denominator x, where x ≠ 0"],["3 is the numerator in 3/5","The fraction bar is not the denominator","4/0 is undefined; zero cannot be a valid denominator"]],
    "distributive-law":["Multiplication applied to each term of a sum.",["2(x + 3) = 2x + 6","−3(a − b) = −3a + 3b","(x + 2)(x + 1) = x² + 3x + 2"],["2(x + 3) = 2x + 3 is false","a(b + c) = ab + c is false","(x + 2)² = x² + 4 is false"]],
    "equation":["Statement asserting equality of two expressions.",["x + 4 = 9","2y = 10","x² − 4 = 0"],["x + 4 is an expression","x > 3 is an inequality","x ∈ A is a membership relation"]],
    "equivalence":["Identical values on their shared permitted domain.",["2(x + 1) and 2x + 2","(x + 1)² and x² + 2x + 1","x² − 4 and (x − 2)(x + 2)"],["2x + 2 and 2x + 3","(x + 1)² and x² + 1","3(x + 2) and 3x + 2"]],
    "estimate":["Reasoned approximation, not necessarily exact.",["49 × 21 is about 1,000","π is approximately 3.14","A room is roughly 8 m long"],["3 + 4 = 7 is exact","A random guess with no estimation method","Writing π = 3.14 as an exact equality"]],
    "event":["Subset of a sample space.",["Even result on a die: {2,4,6}","Heads from a coin toss: {H}","Any result of a die roll: {1,2,3,4,5,6}"],["Rolling a die is the experiment, not the event","1/6 is a probability, not an event","A bare outcome label 4 is not a set of outcomes"]],
    "expand":["Uses distribution to rewrite a product.",["2(x + 3) → 2x + 6","(x + 1)(x − 1) → x² − 1","−3(2y − 1) → −6y + 3"],["2x + 6 → 2(x + 3) is factorising","x + x → 2x is collecting terms","x + 2 = 5 → x = 3 is solving"]],
    "expression":["Represents a mathematical value; asserts no relation.",["7","x + 4","sin θ"],["x + 4 = 9 is an equation","x < 2 is an inequality","x ∈ A is a membership statement"]],
    "factor":["A quantity in a multiplication.",["2 and 6 are factors in 2 × 6","x + 3 and x − 1 are factors in (x + 3)(x − 1)","5 and x are factors of 5x"],["5 and x in 5 + x are addends","7 in x + 7 is an additive term","The + symbol does not denote multiplication"]],
    "factorisation":["Expressing a quantity as a product.",["x² − 9 → (x − 3)(x + 3)","6x + 9 → 3(2x + 3)","x² + 5x + 6 → (x + 2)(x + 3)"],["2(x + 3) → 2x + 6 is expansion","3x + 2x → 5x is collecting terms","x + 2 = 5 → x = 3 is solving"]],
    "function":["Each allowed input has exactly one output.",["f(x) = x² for real x","f(x) = x + 1 for integer x","1 ↦ 3 and 2 ↦ 5 under f(x) = 2x + 1"],["Input 1 assigned both outputs 2 and 3","x² + y² = 1 does not give one y for each x","y = ±√x is not single-valued for x > 0"]],
    "generalisation":["Claim extending beyond observed examples.",["Even + even is even","n(n + 1) is even for every integer n","a + b = b + a for real numbers"],["Only checking 2 + 4 = 6","Only checking 3 + 5 = 8","A conjecture based on a single case without broader justification"]],
    "heuristic":["Useful strategy, not a guaranteed algorithm.",["Try a simpler case","Draw a diagram","Work backwards from the answer"],["A guaranteed long-division algorithm","A mathematical proof","A fully specified mechanical routine"]],
    "identity":["True for every permitted value.",["(a + b)² = a² + 2ab + b²","sin²θ + cos²θ = 1","x + 0 = x"],["x + 2 = 5 holds only for x = 3","x² = 4 is not true for every x","sin θ = 1 holds only at certain angles"]],
    "inequality":["Compares values with an order relation.",["x > 2","3 ≤ 4","−1 < 0"],["x = 2 is an equation","x + 1 is an expression","x ∈ A describes membership, not order"]],
    "intersection":["Elements shared by the sets.",["{1,2} ∩ {2,3} = {2}","{a,b} ∩ {c} = ∅","A ∩ A = A"],["A ∪ B is the union","A \\ B is set difference","A △ B is symmetric difference"]],
    "like-terms":["Same variable factors with identical exponents.",["3x and −7x","2x²y and 5x²y","5 and −2 are constant terms"],["x and x²","x²y and xy²","3a and 3b"]],
    "linear-expression":["No products of variables or powers above one; at least one variable term is present. A constant term is allowed. In strict linear algebra, a non-zero constant term makes the expression affine.",["3x + 2","2x − 5y + 7","−4a + b","x − 3z"],["xy + 2","x² + 1","1/x + 4","5 is constant (degree zero)"]],
    "mathematical-model":["Uses mathematics to represent and analyse reality.",["d = vt for constant speed","P = 2l + 2w for a rectangle","y = mx + c for an approximate trend"],["An opinion with no mathematical representation","An unrelated graph","A numerical guess with no stated assumptions"]],
    "principle":["Underlying mathematical justification.",["The distributive law","The equality substitution principle","Pythagoras’ theorem for right-angled triangles"],["A mnemonic without mathematical justification","A copied numerical answer","A rule used outside its assumptions"]],
    "mean":["For n numerical observations, add all n values and divide by n, with n>0.",["2, 4, 9 have mean 5","4, 4, 4 have mean 4","1, 2, 3, 10 have mean 4"],["The median of 1, 2, 9 is 2 (the mean is 4)","The mode of 2, 2, 5 is 2 (the mean is 3)","Adding observations but not dividing by their count"]],
    "median":["Middle value after ordering; average two central values if even.",["1, 3, 9 have median 3","1, 2, 8, 10 have median 5","5, 5, 5 have median 5"],["The mean need not be the median","The largest value is not generally the median","The mode need not be the median"]],
    "mode":["A data set may have two or more most-frequent values. The mode is not necessarily the mean.",["1, 2, 2, 3 have mode 2","1, 1, 2, 2 have two modes, 1 and 2","Red, blue, red has mode red"],["1, 1, 1, 9 has mean 3 but mode 1","1, 2, 3 has median 2 but no unique mode","1, 1, 9 has largest value 9 but mode 1"]],
    "numerator":["Part of a fraction above the bar.",["3 in 3/5","x + 1 in (x + 1)/4","0 in 0/7"],["5 in 3/5 is the denominator","The fraction bar is not a numerator","7 in 2/7 is the divisor"]],
    "outcome":["One possible result of a trial.",["Rolling a 4 on a die","Getting heads on one coin toss","Drawing a heart when classifying card suit"],["Even roll {2,4,6} is an event containing multiple outcomes","The whole sample space is not one outcome","P(4) = 1/6 is a probability, not an outcome"]],
    "parameter":["Fixed in one model, variable across models.",["m in y = mx + c for a chosen line","r in C = 2πr for a particular circle","p in a binomial probability model"],["x as the variable input to y = mx + c","n as a sequence position index","y as the variable output of a function"]],
    "polynomial":["No negative or fractional exponents on variables; coefficients may be real numbers or parameters.",["3x² − 2x + 7","2xy² + 5","7 (a constant polynomial)"],["1/x","√x","x⁻² + x"]],
    "probability":["Between 0 and 1 inclusive; measures likelihood.",["P(A) = 0 for an impossible event","P(heads) = 1/2 for a fair coin","P(S) = 1 for the sample space"],["P(A) = 1.4 is impossible","P(A) = −0.2 is impossible","P(A) = 120% is impossible"]],
    "procedural-fluency":["Accurate, flexible, efficient method selection and execution.",["Solve 2x + 3 = 9 accurately","Calculate 25 × 4 mentally","Check a solution by substitution"],["Remembering rules but unable to apply them","Repeated avoidable calculation errors","Always selecting a cumbersome method without judgement"]],
    "procedure":["Ordered actions to complete a task.",["Sum and divide to calculate a mean","Long multiplication","Constructing a perpendicular bisector"],["An isolated final answer","A random guess","A drawing without an organised set of steps"]],
    "proof":["Logical argument covering every case under assumptions.",["Prove even + even is even using 2m + 2n","Derive (a + b)² by distribution","Prove the sum of the angles of a triangle is 180° in Euclidean geometry"],["Testing 100 numerical cases","A diagram that merely looks correct","An unsupported assertion"]],
    "representation":["Mathematical idea shown in varied forms.",["A Venn diagram of two sets","A graph of y = 2x + 1","A table of corresponding x and y values"],["An unrelated doodle","A decorative icon with no mathematical meaning","An unlabelled picture that misrepresents the quantities"]],
    "sample-space":["Set of all possible outcomes.",["One coin: {H,T}","One die: {1,2,3,4,5,6}","Two coins: {HH,HT,TH,TT}"],["{2,4,6} omits odd die outcomes","{H} omits tails in a coin toss","{1,2,3,4,5} omits 6 from a standard die"]],
    "simplify":["Equivalent rewriting suited to a purpose.",["2x + 3x → 5x","6/8 → 3/4","√50 → 5√2"],["2x + 3x → 6x is incorrect","6/8 → 2/4 changes the value","(x + 1)² → x² + 1 is incorrect"]],
    "solution-set":["Every value satisfying a stated relation and domain.",["x² = 4 over ℝ: {−2,2}","x > 1 over ℝ: (1,∞)","x + 3 = 3 over ℤ: {0}"],["{2} omits −2 for x² = 4 over ℝ","{0} is not the solution set of x > 1","An equation itself is not a set of its solutions"]],
    "strategic-competence":["Formulate, represent, choose and solve.",["Represent a word problem with a diagram","Choose substitution or elimination appropriately","Check whether an answer is reasonable"],["Blindly substitute numbers without interpreting the problem","Refuse to consider alternative strategies","Apply an unsuitable formula automatically"]],
    "surface-area":["Combined outside area of a solid; square units.",["Cube of side 2 cm: 24 cm²","Cuboid 2 × 3 × 4 cm: 52 cm²","Sphere of radius 1 cm: 4π cm²"],["Cube volume 8 cm³ is not surface area","One face of the cube, 4 cm², is not its total surface area","An edge length 2 cm is not an area"]],
    "term":["Additive part of an expression, including its sign.",["3x and −5 are terms in 3x − 5","x², 4x, and 7 are terms in x² + 4x + 7","−y is one term"],["3 and x are factors within the term 3x","Brackets alone are not an additive term","The coefficient 5 in 5x is not itself the whole term"]],
    "union":["Every element in either set, counted once.",["{1,2} ∪ {2,3} = {1,2,3}","A ∪ ∅ = A","A ∪ A = A"],["A ∩ B is intersection","A \\ B is set difference","Listing only shared members gives intersection, not union"]],
    "variable":["Symbol for an unknown or changing quantity.",["x in 2x + 3","n for the number of students","t representing elapsed time"],["The 5 in 2x + 5 is constant","π is a mathematical constant","cm is a unit of measurement, not a variable"]],
    "volume":["Three-dimensional space occupied; cubic units.",["Cuboid 2 × 3 × 4 cm: 24 cm³","Cube side 3 cm: 27 cm³","Cylinder of radius 1 cm and height 2 cm: 2π cm³"],["Surface area is measured in cm²","Base area alone is not volume","Height in cm is a length, not volume"]],
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
