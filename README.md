# HV World

HV World: the showcase of products built by Harsh Vittori: **https://harshvittori.github.io/**

| App | What it does | Link |
|---|---|---|
| HV Vault | Applications and opportunities, organised, with the HV AI assistant | https://harshvittori.github.io/hv-vault-web/ |
| HV Reset | A calm daily plan: one block, one task | https://harshvittori.github.io/harsh-reset/ |
| HV Test | Free self-assessment tests | https://harshvittori.github.io/hv-tests/ |

## Edit the page

- The page source is `src/page.html`. Logos are the SVG files in `src/`.
- Rebuild with `python3 src/build.py .`. This writes `index.html` and `favicon.svg` and gives every logo copy its own ids.
- LinkedIn: set `LINKEDIN_URL` near the bottom of `src/page.html`, then rebuild. The footer link appears only when it's set.

GitHub Pages serves this repo from the `main` branch at the site root. Keep `.nojekyll`.
