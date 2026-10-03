# Indle — Daily Word Puzzle

The official prelaunch Indle website: six languages, one daily word. Native static
HTML, CSS and a small JavaScript file keep the site fast without a framework or
package installation. The site adds no tracking, cookies, forms or backend.

## Local preview

Python 3.12 or newer is sufficient:

```powershell
python tools/build.py
python -m http.server 4173 --bind 127.0.0.1 --directory ..
```

Open `http://127.0.0.1:4173/Indle-site/`. Serving the parent directory preserves the
GitHub project path, including the nested-route 404 asset paths. The validated
deployment artifact is written to `dist/` and ignored by Git. No build tools or
package manager are required.

## Pages deployment

This repository is intended to be public as `VanarpSuriv/Indle-site`. The Android
repository is separate and must stay private. In this repository's **Settings →
Pages**, select **GitHub Actions** as the source. A push to `main` runs validation,
uploads only `dist/`, and deploys to Pages. The default URL is
`https://vanarpsuriv.github.io/Indle-site/`.

The workflow follows [GitHub's custom Pages workflow documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).
After publication, verify the Actions run, HTTPS landing page, privacy and deletion
pages, mobile navigation, all fonts and images, and a nonexistent nested route.
Local build success does not prove that deployment succeeded.

## Custom domain: indle.tech

Ownership is not yet verified. No domain has been connected and no DNS changes
have been made. Once ownership is established:

1. Add `indle.tech` in the GitHub account's Pages domain settings. Create the exact
   TXT verification record GitHub supplies at
   `_github-pages-challenge-VanarpSuriv.indle.tech`; its value cannot be invented.
   Complete verification and retain the TXT record.
2. Change all canonical, sitemap, robots and social-image URLs to
   `https://indle.tech/`. Change the absolute `/Indle-site/` references in
   `404.html` to `/`. Keep relative assets on other pages.
3. Set `indle.tech` in the repository's Pages custom-domain setting. For an apex
   domain, add four `A` records at `@`:
   `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`.
   For `www`, add a `CNAME` pointing to `vanarpsuriv.github.io` (no repository path).
4. Allow DNS and certificate issuance to finish, then enable **Enforce HTTPS**.
   Check both apex and `www` URLs. Do not use wildcard DNS.

A `CNAME` file is not required by a custom Actions publishing workflow. Configure
the domain in Pages settings. These records are preparation instructions, not a
claim of ownership or active configuration. See [domain configuration](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)
and [verification](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages).

## Public content and release boundaries

The six native names are language identity labels. The only app image is an
approved empty Tamil board from a real development build. No puzzle answers,
clues, dictionaries, review files, account details or credentials are included.
The interactive demo is clearly labeled an abstract interaction study. It does
not present fabricated app screenshots or a playable game.

The website is a prelaunch preview. All language content requires release review.
AI defaults off; voice and pronunciation are not advertised as available. Cloud
and deletion flows still need release verification. A monitored private support
and external deletion request channel, verified publisher legal identity and
retention schedule are missing. The privacy and deletion pages state these limits
openly; they are not a finalized Play Store privacy policy or working external
deletion request resource. Public issues accept non-sensitive technical feedback
only.

## Asset licenses

Site code: MIT. App image: owner-authorized Indle development screenshot. Noto
script fonts: SIL Open Font License, complete notices beside the files. See
`assets/ASSETS.md`. No remotely loaded fonts or visual libraries are used.

## Public repository allowlist

The build script lists exact deployment files. The public source repository adds
only `README.md`, `LICENSE`, `SECURITY.md`, `.gitignore`,
`.github/workflows/pages.yml`, `tools/build.py`, and `assets/ASSETS.md`. Do not copy
anything from the private app repository outside that reviewed list.
