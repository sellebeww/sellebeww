# Profile assets and maintenance

The README is the deliverable. Its layout uses GitHub Markdown, supported HTML, and local images. It does not depend on a website, JavaScript, remote stats widgets, custom README CSS, or external SVG resources.

## Files

```text
README.md
assets/
├── profile.png           # Actual public GitHub avatar, stored as PNG
├── background.png        # Original generated artwork; retain as the master
├── background.jpg        # Optimized artwork embedded in the SVG compositions
├── hero.svg              # Desktop artwork + glass UI + profile photo
├── hero-mobile.svg       # Dedicated portrait composition for narrow screens
├── divider.svg           # Quiet animated glow; supports reduced motion
├── footer.svg            # Desktop closing scene
├── footer-mobile.svg     # Readable mobile closing scene
├── github-data.json      # Timestamped snapshot of real GitHub data
├── stats.svg             # Repository count, contributions, streaks, stars, followers
├── languages.svg         # Primary-language counts across non-fork public repos
├── activity.svg          # One year of daily contribution history
└── activity-mobile.svg   # Last 16 weeks, with larger cells
scripts/
├── generate-assets.py    # Rebuild hero, dividers, and footer
└── update-stats.py       # Fetch public data and rebuild statistics
.github/workflows/
└── profile-stats.yml     # Daily/manual refresh of checked-in statistics
```

Keep these paths relative to the root README. The PNG/JPEG inputs and avatar are embedded as data URIs in the SVGs, so the rendered images make no nested network requests. Keep the source assets to make future regeneration possible. The dragon and fog are one original composition; separate `creature.png`, `fog.gif`, and `particles.gif` files are unnecessary. Motion is limited to the divider's slow glow, and a static frame remains complete if animation is disabled.

## Rebuild the visuals

Python 3.10+; no packages to install:

```sh
python3 scripts/generate-assets.py
python3 scripts/update-stats.py --offline
```

To change the avatar, replace `assets/profile.png` with a real PNG and regenerate. Change text, composition, and palette in `scripts/generate-assets.py`. Desktop and mobile typography have separate layouts. The artwork's exact generation prompt is in [artwork-prompt.md](./artwork-prompt.md); it was generated using the built-in image generation tool, with code-native SVG UI added separately.

The hero's “BUILDING SOMETHING” indicator describes creative focus; it is not a live online/presence indicator.

## Statistics

The committed snapshot works immediately, including before Actions is enabled. The workflow is configured for 01:17 UTC / 08:17 WIB daily and can be run manually from **Actions → Refresh profile statistics → Run workflow** after publishing it to the default branch. Scheduled runs may be delayed by GitHub.

It uses the repository's built-in `GITHUB_TOKEN` with `contents: write` to query the public GitHub API and commit updated assets. No personal access token or third-party statistics server is required for the workflow. Repository or organization rules must allow Actions to push; protected branches may require adapting the workflow to open a pull request. If a refresh fails, the previous committed cards remain available and show their snapshot date. This workflow has been prepared locally; a hosted Actions run has not been performed.

For an authenticated local refresh, expose a GitHub token as `GITHUB_TOKEN` in your environment, then run:

```sh
python3 scripts/update-stats.py
```

Never put tokens in the README, SVGs, snapshot, or git history.

Definitions:

- **Public repos** and **followers**: GitHub's public user counts.
- **Stars**: stars on owned, public, non-fork repositories.
- **Contributions**: GitHub's contribution calendar for the past year, not a raw commit count.
- **Current streak**: consecutive active calendar days at the snapshot date; an unfinished zero-contribution final day does not break the streak yet.
- **Best streak**: longest active streak inside the fetched year, not an all-time record.
- **Language signal**: number of non-fork public repositories with each primary language; top five shown. This is neither byte share nor skill level.
- **Mobile activity**: last 16 weeks; the desktop card displays the full fetched calendar.

## Profile publishing

This checkout currently points to `sellebeww/sellebeww-profile`. GitHub displays a profile README from the public repository matching the username: **`sellebeww/sellebeww`**. Publish `README.md`, `assets/`, `scripts/`, and `.github/workflows/` together in that repository to use this design on the account profile. No remote rename, commit, push, or repository creation was performed as part of this redesign.

See [GitHub's profile README requirements](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme).

## Content and contacts

Name, username, interests, and location were retained from the original README. Project names, links, stack descriptions, avatar, and portfolio URL were checked against the public GitHub profile and repository metadata. The four featured artifacts are real repositories. Project labels describe the available repository/demo; they do not imply production readiness.

Only verified GitHub and portfolio links appear publicly. If you want LinkedIn or email, add your actual URLs to **Enter the signal**. Optional templates (replace values before adding):

```md
[LinkedIn ↗](https://www.linkedin.com/in/YOUR_LINKEDIN/)
[Email ↗](mailto:YOUR_EMAIL)
```

## Compatibility checks

The README was rendered through GitHub's Markdown API. Its returned HTML was previewed locally with GitHub-style Markdown CSS at desktop, 390 px, and 320 px widths, plus light mode. This checks Markdown sanitization and browser layout; it is not a screenshot of a published profile. Live GitHub caching and the hosted Actions workflow are only exercised after publication.

Saved first-screen previews: [desktop](./preview-desktop.png) and [mobile](./preview-mobile.png). All local images loaded, section anchors resolved, and no horizontal overflow was detected at the checked widths. The stats updater also completed a real API refresh; streak boundary cases and SVG XML parsing passed. The advertised Batch Aman demo returned HTTP 404, so only its verified source repository is linked. The portfolio and F&B demo returned HTTP 200.

SVGs use standard image elements, embedded images, gradients, clip paths, and text. No scripts, `foreignObject`, remote fonts, or linked CSS. Important portfolio content, project links, and contact links stay in native Markdown; hero identity and image descriptions also have accessible text alternatives. Reduced-motion preferences disable the divider glow.
