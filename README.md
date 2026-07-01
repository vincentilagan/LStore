# LStore — The Luci OS App Store

The official app store for **Luci OS**, published by **Vincent Ilagan**.

- **Live site:** `index.html` is a static storefront (deployable on Render.com).
- **In-OS:** the `LStore.vx` app opens this store inside Luci. Clicking **Install**
  downloads the app's `.vx` straight into `~/Applications` / the programfiles.
- **Catalog:** [`apps.json`](apps.json) is the machine-readable list the store reads.
- **App files:** every app's `.vx` lives under [`/apps`](apps). Install = fetch that file
  (a lightweight "git clone" of a single app).

## For developers — publish your app

1. Add your `.vx` under `/apps/<yourapp>.vx`.
2. Add an entry to `apps.json` (id, name, version, author, category, icon, summary,
   `install` path).
3. Open a pull request.

Third-party apps do **not** need to be signed to be listed. Luci's **Cosmic Guard**
protects the user at launch: an unsigned/untrusted app triggers an *"Allow this app?"*
prompt and cannot touch guarded system or network APIs until the user allows it.
First-party apps signed by Vincent Ilagan run trusted and silent.

## Roadmap

- Render.com live deploy of `index.html`.
- Native install bridge in `LStore.vx` (`window.LStoreNative.install`).
- Migration from GitHub hosting to a dedicated server.

---

© Vincent Ilagan · Luci OS
