# Book — Mathematics

An open, student-centred Mathematics textbook authored in [PreTeXt](https://pretextbook.org/).

## Editing and building

This repository is the authoritative source. You can edit through GitHub Codespaces or clone it into VS Code on Windows.

- Run `python -m pip install -r requirements.txt` to install PreTeXt.
- Run `pretext build web` to generate the HTML textbook in `output/web`.
- Run `pretext view web` for a local preview.
- GitHub Actions builds and publishes the web edition when changes are pushed to `main`.

Enable GitHub Pages under **Settings → Pages → Build and deployment → Source: GitHub Actions**.

The web address, when deployed, is https://ronandownes.github.io/book/ .

The structure deliberately separates strands into Parts rather than strictly following curriculum strands. We are building for independent learning: notice, predict, explore, explain, practise, connect and assess.

Runestone integration will be configured as a distinct publishing target when the public HTML build is stable. Student accounts and response tracking are not yet configured.
