/* Audit the glossary's pedagogical coverage and its original diagrams.
   Run: node scripts/audit_glossary_data.js */
const fs = require("node:fs");
const vm = require("node:vm");
const assert = require("node:assert/strict");
const source = fs.readFileSync("assets/frayer-glossary.js", "utf8");
const xml = fs.readFileSync("source/shared-glossary.ptx", "utf8");
const entries = [...xml.matchAll(/<gi xml:id="glossary-([^"]+)"/g)].map(m => m[1]);
const dataMatch = source.match(/const data = (\{[\s\S]*?\n  \});/);
assert(dataMatch, "Glossary data not found");
const data = vm.runInNewContext("(" + dataMatch[1] + ")");
assert.equal(Object.keys(data).length, entries.length, "Each glossary term needs examples");
for (const slug of entries) {
  const item = data[slug];
  assert(item, "Missing glossary term: " + slug);
  assert.equal(item.length, 3, "Expected characteristics/examples/non-examples for " + slug);
  assert.equal(typeof item[0], "string", "Characteristics missing: " + slug);
  for (const [index, label] of [[1,"examples"],[2,"non-examples"]]) {
    assert(Array.isArray(item[index]), "Expected list of " + label + " for " + slug);
    assert(item[index].length >= 3 && item[index].length <= 4,
      slug + " needs three or four " + label);
    for (const example of item[index]) assert(typeof example === "string" && example.trim(),
      "Blank " + label + " in " + slug);
  }
}
const visualsMatch = source.match(/const glossaryVisuals = (\{[\s\S]*?\});\n  function diagramFor/);
assert(visualsMatch, "SVG illustration catalogue missing");
const visuals = JSON.parse(visualsMatch[1]);
for (const slug of ["area","intersection","union","absolute-value","function","sample-space","volume","surface-area"]) {
  assert(visuals[slug], "Missing visual: " + slug);
  assert(visuals[slug].includes("role=\"img\""), "Accessible SVG missing: " + slug);
}
assert(visuals.area.includes("Simpson"), "Area needs Simpson's rule diagram");
assert(visuals.area.includes("four equal intervals"), "Simpson's rule must use an even number of intervals");
assert(visuals.area.includes("4y₂ + 2y₃ + 4y₄"), "Wrong Simpson's rule coefficients");
assert(!source.includes("Explore Frayer diagram"), "Jargon-labelled button must not reappear");
console.log("Verified " + entries.length + " glossary terms, 3–4 examples and non-examples each, and " +
  Object.keys(visuals).length + " diagram entries.");
