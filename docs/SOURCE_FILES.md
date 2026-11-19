# Finding and editing the book source

The source stays in one flat folder. Filenames group alphabetically by course,
strand and topic. Existing TY chapter files remain under `source/ty/`.

| Prefix | Material |
| --- | --- |
| `jc-number-` | Junior Cycle Number |
| `jc-algebra-` | Junior Cycle Algebra and Functions |
| `jc-geometry-` | Junior Cycle GT learning outcomes, GT.3 Synthetic Geometry chapter and generated GT.3/GT.4 outcome sections |
| `jc-trigonometry-` | Junior Cycle Trigonometry |
| `jc-statistics-` | Junior Cycle Statistics and Probability learning outcomes |
| `lc-ol-number-` | Leaving Certificate Ordinary Level Number |
| `lc-ol-algebra-`, `lc-ol-functions-`, `lc-ol-geometry-`, `lc-ol-statistics-` | Other LC Ordinary Level strands |
| `shared-` | Shared reference material and teaching source not assigned to a course |
| `draft-` | Future draft material |

For example, edit `source/jc-algebra-factorisation.ptx` for Factorisation,
`source/jc-number-fractions.ptx` for Fractions, and
`source/lc-ol-number-complex-numbers.ptx` for Complex Numbers.

`source/main.ptx` assembles the book and sets its order. The Functions and
Graphs and Events and Counting chapters currently have their text in that file.
Source filenames do not set printed chapter numbers or public page addresses:
preserve the existing `xml:id` values when editing.

## Geometry and Trigonometry: one source, six GT chapters

The official NCCA source data is processed by `scripts/build_intro_outcomes.py`
into a six-outcome table and by `scripts/build_outcome_pages.py` into
the `source/jc-geometry-outcomes.ptx` chapter with the single complete
**GT Learning Outcomes** overview.

**Never type an official learning outcome into a teaching chapter.** The
same generator writes all six `source/jc-geometry-gtN-outcome.ptx` quotations
directly from that authoritative table. Each GT chapter uses an
`xi:include` of its quotation inside its introduction. This guarantees
the text in the overview and chapter opening is identical; the HTML
build validator compares every official paragraph and inline annotation.

The main book orders these six chapters after the overview:

- GT.1: `jc-geometry-gt1-measurement.ptx`
- GT.2: `jc-geometry-gt2-shapes-solids.ptx`
- GT.3: `jc-geometry-synthetic-geometry.ptx`
- GT.4: `jc-trigonometry-ratios-triangles.ptx`
- GT.5: `jc-geometry-gt5-coordinate-plane.ptx`
- GT.6: `jc-geometry-gt6-transformations.ptx`

GT.1, GT.2, GT.5 and GT.6 are intentionally minimal teaching-chapter
shells containing the exact official outcome, ready for future lessons.
GT.3 and GT.4 retain their existing teaching material. The blue
learning-outcome quotation is distinct from purple, author-written
`objectives` (Learning Intentions). No separate numbered GT outcome
sections clutter the table of contents. The older GT outcome URLs
redirect to the corresponding chapter introductions.

## Learning outcomes and publishing

The numbered official outcome files are regenerated during the build by
`scripts/build_intro_outcomes.py` and `scripts/build_outcome_pages.py`.
Corrections to that generated material belong in those generators.
The chapter files above are edited directly.

Saving changes to `main` starts the Build and publish PreTeXt book workflow.
Check that its build and deployment both succeed before refreshing the live book.

## Filename changes

The following source files were renamed together with their include paths and
build-script references. Course content, identifiers and publication order were
preserved. Files already using consistent course prefixes retained their names.

| Previous filename | Current filename |
| --- | --- |
| `accuracy-standard-form.ptx` | `jc-number-accuracy-rounding.ptx` |
| `algebra-changing-subject.ptx` | `jc-algebra-changing-subject.ptx` |
| `algebra-division-fractions.ptx` | `jc-algebra-division-fractions.ptx` |
| `algebra-equations-inequalities.ptx` | `jc-algebra-equations-inequalities.ptx` |
| `algebra-factorisation.ptx` | `jc-algebra-factorisation.ptx` |
| `algebra-language.ptx` | `jc-algebra-language.ptx` |
| `algebra-patterns.ptx` | `jc-algebra-patterns.ptx` |
| `algebra-simplifying.ptx` | `jc-algebra-simplifying.ptx` |
| `algebra-substitution.ptx` | `jc-algebra-substitution.ptx` |
| `arithmetic.ptx` | `jc-number-operations.ptx` |
| `complex-numbers-chapter.ptx` | `lc-ol-number-complex-numbers.ptx` |
| `decimals-percentages.ptx` | `jc-number-decimals-percentages.ptx` |
| `expanding-brackets.ptx` | `jc-algebra-expanding-brackets.ptx` |
| `expansions-like-factors.ptx` | `jc-algebra-expansions-like-factors.ptx` |
| `expansions-unlike-factors.ptx` | `jc-algebra-expansions-unlike-factors.ptx` |
| `factors-multiples-primes.ptx` | `jc-number-factors-multiples-primes.ptx` |
| `financial-mathematics.ptx` | `shared-financial-mathematics.ptx` |
| `fractions.ptx` | `jc-number-fractions.ptx` |
| `glossary.ptx` | `shared-glossary.ptx` |
| `index-laws.ptx` | `jc-number-index-laws.ptx` |
| `indices-roots.ptx` | `jc-number-powers-roots.ptx` |
| `lc-ordinary-official-outcomes.ptx` | `lc-ol-official-outcomes.ptx` |
| `number-graphs.ptx` | `jc-number-graphs.ptx` |
| `number-introduction.ptx` | `jc-number-representation.ptx` |
| `number-patterns.ptx` | `jc-number-sequences.ptx` |
| `number-systems.ptx` | `jc-number-systems.ptx` |
| `order-of-operations.ptx` | `jc-number-order-of-operations.ptx` |
| `ratio-proportion.ptx` | `jc-number-ratio-proportion.ptx` |
| `scientific-notation.ptx` | `jc-number-scientific-notation.ptx` |
| `sequences-chapter.ptx` | `lc-ol-number-sequences-series.ptx` |
| `sequences-families.ptx` | `lc-ol-number-sequences-families.ptx` |
| `sequences-foundations.ptx` | `lc-ol-number-sequences-foundations.ptx` |
| `sequences-resources.ptx` | `lc-ol-number-sequences-resources.ptx` |
| `sequences-rules.ptx` | `lc-ol-number-sequences-rules.ptx` |
| `sequences-series-introduction.ptx` | `lc-ol-number-sequences-series-introduction.ptx` |
| `sets-chapter.ptx` | `jc-number-sets.ptx` |
| `specifications.ptx` | `shared-specifications.ptx` |
| `trigonometry-chapter.ptx` | `jc-trigonometry-ratios-triangles.ptx` |
| `unifying-strand.ptx` | `jc-unifying-strand.ptx` |
| `vectors-future-draft.ptx` | `draft-vectors.ptx` |
