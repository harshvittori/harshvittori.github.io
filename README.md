# HV World

**https://harshvittori.github.io/** tells the story of three products built by Harsh Vittori.

Growth breaks at three links. HV World fixes each one and joins them into a chain: **Know → Plan → Act → Grow**.

| Link | Product | The problem it solves | Link |
|---|---|---|---|
| 1 · Know | HV Test | Guessing your own strengths | https://harshvittori.github.io/hv-tests/ |
| 2 · Plan | HV Reset | Days that drift | https://harshvittori.github.io/harsh-reset/ |
| 3 · Act | HV Vault | Opportunities that slip | https://harshvittori.github.io/hv-vault-web/ |

## The story

The page follows one person, Riya, as a scroll-driven cartoon:

1. **Prologue**: Riya at her desk late at night, stuck on three questions.
2. **Chapter 1, HV Test**: she freezes in an interview, takes the test, sees her score, and answers the next interview with confidence.
3. **Chapter 2, HV Reset**: her day slips away, HV Reset turns it into blocks, a late start shifts the plan, and everything is ticked by evening.
4. **Chapter 3, HV Vault**: opportunities float away, HV Vault puts them on one board, HV AI reminds her, and the offer arrives.
5. **Finale**: the three products joined as a chain, Know, Plan, Act, then grow and go again.

As you scroll, each caption changes the picture beside it (on phones, the picture stays at the top and the captions scroll under it).

## Edit the page

- Everything is in `src/story.py`: the characters and scenes (SVG), the captions, the CSS animations and the page text. The logos are the SVG files in `src/`.
- Rebuild from the repo root with `python3 src/story.py`. This writes `index.html` and `favicon.svg`.

## The overview page

**https://harshvittori.github.io/overview/** is the full product tour: every app with its features and a preview, how they work together, HV AI, privacy, price (₹0) and an FAQ. It uses the original orbit logo (`src/world-orbit.svg`).

- Everything is in `src/overview.py`. Rebuild with `python3 src/overview.py`. This writes `overview/index.html`.
- The two pages link to each other ("All features" and "Riya's story").

GitHub Pages serves this repo from `main` at the site root. Keep `.nojekyll`.
