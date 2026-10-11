# Security

This repository contains only the public static Indle website. Its account-deletion page loads the pinned Firebase web SDK and accepts an explicit
Google-authenticated deletion action through the existing Supabase service. It stores
no credentials or sessions in browser storage. No analytics or private app code is published.

For a non-sensitive website bug, use this repository's issues. Never post account
information, credentials, personal data, or deletion requests in public issues.
Private vulnerability reporting should be enabled in this repository's Security
settings before accepting sensitive reports. No monitored private email is
currently advertised.

The build uses an exact public-file allowlist and checks for credential patterns,
unexpected files and missing links. Review the staged diff before every push.
Never add Android source, content packs, raw review material, private configuration,
environment files or internal build outputs. Keep the Android repository private.

GitHub Actions has read-only default repository access. Only the deployment job
receives Pages and OIDC write permissions. Deployments target the github-pages
environment and are serialized.
