# Security

This repository contains the public static Indle website and its optional authenticated account-deletion page. The page uses pinned Firebase SDK modules, memory-only account state and the existing Indle Edge deletion endpoint. It stores no private keys or service-role credentials. No analytics or private Android source is included.

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

The deletion form is the only allowlisted form. Its target identity is derived by the server from a verified bearer token and recent authentication. CSP and Referrer Policy meta controls are local browser policies, not configurable GitHub Pages HTTP headers. Frame-ancestors, X-Frame-Options, Permissions-Policy and X-Content-Type-Options require hosting/proxy support; no meta-tag substitute is claimed. Do not deploy changes or perform live destructive account tests without authorization.
