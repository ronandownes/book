# Integrated Mathematics: implementation notes (draft)

This document is an implementation plan on a feature branch, not a change to the published book.

## Four connected tools

- **A — Apps:** visual exploration, interactive questioning, assessment as learning.
- **B — Book:** one coherent mathematical story, organised as Part I Junior Cycle and Part II Leaving Certificate, with explicit prerequisite and extension links between them.
- **C — Calculator:** topic-specific guided demonstrations, watch/follow/independent practice. A demonstration should operate the emulator state directly, not require an exported video.
- **D → P — Past Papers:** search by topic/subtopic and mathematical skill, jump to complete question and corresponding marking scheme, select and print worksheets.

## Printed question collections

Every question has an immutable source ID, for example `JC-H-2005-P1-Q04-b`. Printed page labels are **edition-specific**, such as `CA 12` or `LC · Statistics · Correlation · 3`. They must never act as database IDs.

An exported PDF records its chosen filters, edition, creation date, selected question IDs, and page-to-question mapping. Keep full original paper pages as a first stage, then add verified question-region cropping.

## Classroom-first milestone

1. Preserve existing source PDFs and existing printed numbering; do not overwrite.
2. Build selection of verified questions by topic, year and level.
3. Generate a student question-only PDF with a descriptive header and contiguous numbering *within that PDF*.
4. Generate a separate teacher solutions version, linking each question to an available official marking scheme.
5. Verify printed output (A4) and classroom projection.
6. Keep publication and student distribution behind explicit teacher approval.

## Pedagogical principles

- Build conceptual understanding, accurate and flexible procedural fluency, strategic competence, adaptive reasoning and productive disposition.
- Show complete mathematical methods before decomposing them into examination subparts.
- Offer both an interactive worked demonstration and a conventional handwritten-style worked solution.
- Allow learners to revisit foundational material or advance to harder work independently of their current examination level.
- Preserve access to source examination pages and mark schemes with transparent provenance and permissions.

## Delivery safeguards

Do not alter source PDFs, deploy copyrighted source material, expose student data, or publish unfinished classroom resources from this branch. Review and test before merging to main.
