# Mathematics textbook: one source, JC first, LC additions

## Editorial policy

- The Mathematics site is **one PreTeXt book**. Its major parts remain Number, Algebra, Functions, Geometry, Trigonometry, Statistics and Probability, together with the Unifying Strand and Specifications.
- **JC is foundational:** teach core concepts once, using concise mathematical language, diagrams, examples and exercises.
- **LC contains only additional material:** link back to the JC treatment with `<xref ref="existing-id"/>`, even when an LC learning outcome uses slightly different wording.
- Use **JC** and **LC** in reader-facing headings. Do not create a separate JC Ordinary Level textbook or repeat content for Higher Level.
- Identify **Higher Level-only** content within its section, when verified against the official specification.
- Ordinary Level is the baseline for LC; Foundation Level may be addressed separately later.
- Keep **every chapter in its own PTX** file. Section PTX files can be included inside a chapter through XInclude. Do not keep a parallel, manually copied LC edition.
- **Preserve unique `xml:id` identifiers** across moves and future splits. An identifier is a durable target for PreTeXt cross-references and links.
- Some existing content remains mixed, notably Sequences and Series. Classify it carefully by actual JC/LC syllabus before moving it.
- The revised Leaving Certificate Mathematics specification is still in development as of November 2026; do not assume a settled commencement or content until official confirmation.

## Current structure

| Major part | Foundation / shared content | Additional LC material |
| --- | --- | --- |
| Number | Sets; Sequences and Series (needs level audit) | Complex Numbers — LC |
| Algebra | Algebra — JC: Language, Expanding Brackets, Factorisation | Algebra — LC: further topics, initially placeholders |
| Functions | Functions and Graphs | Calculus — LC |
| Geometry | One shared geometry chapter | Add LC-only sections/chapters only when needed |
| Trigonometry | Trigonometry — JC: right triangles, ratios and applications | Trigonometry — LC: rules, triangle area and limiting values |
| Statistics | One shared foundation | Add LC-only material when needed |
| Probability | One shared foundation and counting | Add LC-only material when needed |

This review branch does **not** publish changes to the live textbook. It must first pass `pretext build web` and be reviewed for navigation, cross-references and asset links.
