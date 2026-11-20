# Ibo website

The website of Ibo, the translation app for macOS and Windows: a static site in the same structure and style as Asaki's (`index.html`, `changelog.html`, `privacy.html`, `styles.css`, `site.js`, `assets/`). Both languages are in each page; `site.js` picks the language, and the visitor's system decides which shortcuts are shown and which installer gets the filled button.

## Preview

```sh
python3 -m http.server 4336 --bind 127.0.0.1 --directory .
```

## Screenshots

The pictures in `assets/` are the app's real pages (`../app/app/web`) rendered in headless Chrome against sample data, in Chinese and English:

```sh
python3 -I scripts/screenshots.py assets
```

## Downloads

The download links point at `https://github.com/lhjZY/ibo-releases/releases/latest/download/` with fixed file names, so the page does not change with each version:

| File on the release | Built as |
| --- | --- |
| `Ibo.dmg` | `ibo-<version>.dmg` |
| `Ibo-Setup-x64.exe` | `ibo-setup-<version>-amd64.exe` |
| `Ibo-Setup-arm64.exe` | `ibo-setup-<version>-arm64.exe` |

For each release, update the version and sizes in `index.html` and add the version to `changelog.html`.
