"""Validate the public source and stage an exact static deployment artifact."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import re
import shutil
import struct
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = (
    "index.html", "privacy.html", "account-deletion.html", "404.html",
    "styles.css", "site.js", "robots.txt", "sitemap.xml",
    "assets/app-board.png", "assets/favicon.svg", "assets/social-card.png",
    "assets/fonts/noto_sans_tamil.ttf", "assets/fonts/NotoSansTamil-OFL.txt",
    "assets/fonts/noto_sans_telugu.ttf", "assets/fonts/OFL-te.txt",
    "assets/fonts/noto_sans_kannada.ttf", "assets/fonts/OFL-kn.txt",
    "assets/fonts/noto_sans_devanagari.ttf", "assets/fonts/OFL-hi.txt",
    "assets/fonts/noto_sans_malayalam.ttf", "assets/fonts/OFL-ml.txt",
)
SOURCE = (*PUBLIC, "README.md", "LICENSE", "SECURITY.md", ".gitignore",
          ".github/workflows/pages.yml", "tools/build.py", "assets/ASSETS.md")


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path, self.ids, self.links = path, set(), []
        self.titles = self.h1s = self.mains = 0

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if attrs.get("id"):
            assert attrs["id"] not in self.ids, f"Duplicate ID in {self.path}"
            self.ids.add(attrs["id"])
        if tag == "title": self.titles += 1
        if tag == "h1": self.h1s += 1
        if tag == "main": self.mains += 1
        if tag == "html": assert attrs.get("lang") == "en"
        if tag == "img":
            assert attrs.get("alt") and attrs.get("width") and attrs.get("height"), self.path
        assert tag not in ("form", "iframe"), f"Unexpected external data surface in {self.path}"
        for name in ("href", "src"):
            if attrs.get(name): self.links.append(attrs[name])


def validate():
    expected = set(SOURCE)
    actual = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*")
              if p.is_file() and not set(p.relative_to(ROOT).parts) & {".git", "dist", "__pycache__"}}
    assert actual == expected, f"File allowlist differs. Extra: {actual - expected}; missing: {expected - actual}"
    credential = re.compile(
        r"A" + r"Iza[0-9A-Za-z_-]{20,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|"
        r"gh[pousr]_[A-Za-z0-9]{30,}|(?:sb_secret_|sk_live_)[A-Za-z0-9_-]{15,}|"
        r"eyJ[A-Za-z0-9_-]{15,}\.eyJ[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{15,}"
    )
    for name in SOURCE:
        path = ROOT / name
        assert not path.is_symlink(), f"Symlink excluded: {name}"
        if path.suffix not in (".png", ".ttf"):
            assert not credential.search(path.read_text(encoding="utf-8")), f"Credential pattern in {name}"
    pages = {}
    for name in PUBLIC:
        if name.endswith(".html"):
            parser = Page(name)
            parser.feed((ROOT / name).read_text(encoding="utf-8"))
            assert (parser.titles, parser.h1s, parser.mains) == (1, 1, 1), name
            pages[name] = parser
    for name, parser in pages.items():
        for link in parser.links:
            url = urlsplit(link)
            if url.scheme:
                assert url.scheme == "https", f"Unexpected scheme: {link}"
                continue
            path = unquote(url.path)
            if path.startswith("/Indle-site/"): path = path[len("/Indle-site/"):]
            elif path.startswith("/"): raise AssertionError(f"Wrong project base: {link}")
            target = (ROOT / name).parent / path if path else ROOT / name
            if target.is_dir(): target /= "index.html"
            assert target.resolve().is_relative_to(ROOT), f"Escaping link: {link}"
            assert target.is_file(), f"Broken link from {name}: {link}"
            if url.fragment:
                target_name = target.relative_to(ROOT).as_posix()
                assert target_name in pages and url.fragment in pages[target_name].ids, f"Missing anchor: {link}"
    for asset in re.findall(r"url\(['\"]?([^)'\"]+)", (ROOT / "styles.css").read_text()):
        assert (ROOT / asset).is_file(), f"Missing CSS asset: {asset}"
    ET.parse(ROOT / "sitemap.xml")
    ET.parse(ROOT / "assets/favicon.svg")
    for name, size in (("app-board.png", (1080, 2400)), ("social-card.png", (1200, 630))):
        data = (ROOT / "assets" / name).read_bytes()
        assert data[:8] == b"\x89PNG\r\n\x1a\n" and struct.unpack(">II", data[16:24]) == size, name
    index = (ROOT / "index.html").read_text(encoding="utf-8")
    for language in ("தமிழ்", "తెలుగు", "ಕನ್ನಡ", "हिन्दी", "മലയാളം", "English"):
        assert language in index, f"Missing language: {language}"
    assert "prefers-reduced-motion" in (ROOT / "styles.css").read_text()
    assert "Coming soon to Google Play" in index
    assert "not available yet" in (ROOT / "account-deletion.html").read_text()
    return pages


if __name__ == "__main__":
    pages = validate()
    # ponytail: exact allowlist replaces a site generator; add one only for repeated editorial content.
    destination = (ROOT / "dist").resolve()
    assert destination.parent == ROOT and destination.name == "dist"
    if destination.exists(): shutil.rmtree(destination)
    for name in PUBLIC:
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / name, target)
    total = sum((destination / name).stat().st_size for name in PUBLIC)
    print(f"PASS: {len(pages)} pages, {len(SOURCE)} reviewed source files, {len(PUBLIC)} deployment files, {total:,} bytes.")
