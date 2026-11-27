# Well Connected Maths

*Revisit. Connect. Extend.*

An open, student-centred Mathematics textbook authored in [PreTeXt](https://pretextbook.org/).

## Editing and building

This repository is the authoritative source. You can edit through GitHub Codespaces or clone it into VS Code on Windows.

Source files use course and strand prefixes, for example `source/jc-algebra-factorisation.ptx`. See [the source file guide](docs/SOURCE_FILES.md) for chapter locations and the filename map.

- Run `python -m pip install -r requirements.txt` to install PreTeXt.
- Run `pretext build web` to generate the HTML textbook in `output/web`.
- Run `pretext view web` for a local preview.
- GitHub Actions builds and publishes the web edition when changes are pushed to `main`.

Enable GitHub Pages under **Settings → Pages → Build and deployment → Source: GitHub Actions**.

The web address, when deployed, is https://ronandownes.github.io/book/ .

This Junior Cycle edition is organised into five Parts, one for each strand: Unifying Strand, Number, Geometry and Trigonometry, Algebra and Functions, and Statistics and Probability. Each Part begins with its official Learning Outcomes. The Number strand currently has thirteen teaching chapters, each with Learning Intentions and an introduction.

The LC Ordinary Level and TY source files are retained in the repository but are not published in this Junior Cycle edition.

We are building for independent learning: notice, predict, explore, explain, practise, connect and assess.

Runestone integration will be configured as a distinct publishing target when the public HTML build is stable. Student accounts and response tracking are not yet configured.
