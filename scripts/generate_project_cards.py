#!/usr/bin/env python3
"""Generate static SVG project cards from GitHub repository metadata.

The cards are generated locally by GitHub Actions, so the README does not
need to call github-readme-stats or any Vercel deployment.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from urllib.request import Request, urlopen


PROJECTS = [
    "https://github.com/HeiKe-Tom/CN-Language",
    "https://github.com/HeiKe-Tom/OPPO_OnePlus_Realme-SM8750-Kernel-Builder",
]

OUTPUT_DIR = Path("assets/projects")

BG = "17150d"
TITLE = "a8c7fa"
TEXT = "e5e5e5"
ACCENT = "a8c0fa"
BORDER = "555555"


def repo_name(url: str) -> str:
    value = url.rstrip("/").split("github.com/", 1)[1]
    return value.split("/", 1)[0] + "/" + value.split("/", 1)[1].split("/", 1)[0]


def fetch_repo(full_name: str) -> dict:
    request = Request(
        f"https://api.github.com/repos/{full_name}",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {os.environ.get('GITHUB_TOKEN', '')}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "HeiKe-Tom-profile-generator",
        },
    )
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def esc(value: object) -> str:
    text = str(value or "")
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def truncate(text: str, length: int) -> str:
    text = " ".join((text or "").split())
    return text if len(text) <= length else text[: length - 1] + "…"


def language_label(repo: dict) -> str:
    language = repo.get("language") or "Code"
    return str(language)


def make_card(repo: dict) -> str:
    full_name = repo["full_name"]
    description = truncate(repo.get("description") or "No description provided.", 68)
    stars = repo.get("stargazers_count", 0)
    forks = repo.get("forks_count", 0)
    language = language_label(repo)
    license_name = (repo.get("license") or {}).get("spdx_id") or "No license"
    updated = (repo.get("pushed_at") or "").replace("T", " ").replace("Z", " UTC")
    updated = updated[:16] if updated else "Unknown"

    # Fixed 840x220 SVG: two cards fit cleanly side-by-side in a README.
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="840" height="220" viewBox="0 0 840 220" role="img" aria-label="{esc(full_name)}">
  <rect x="1" y="1" width="838" height="218" rx="16" fill="#{BG}" stroke="#{BORDER}" stroke-width="2"/>
  <rect x="24" y="24" width="8" height="172" rx="4" fill="#{ACCENT}"/>
  <text x="54" y="58" fill="#{TITLE}" font-family="Segoe UI,Arial,sans-serif" font-size="25" font-weight="700">{esc(full_name)}</text>
  <text x="54" y="94" fill="#{TEXT}" font-family="Segoe UI,Arial,sans-serif" font-size="15">{esc(description)}</text>

  <circle cx="60" cy="137" r="4" fill="#{ACCENT}"/>
  <text x="74" y="143" fill="#{TEXT}" font-family="Segoe UI,Arial,sans-serif" font-size="15">{esc(language)}</text>

  <text x="210" y="143" fill="#{TEXT}" font-family="Segoe UI,Arial,sans-serif" font-size="15">★ {stars}</text>
  <text x="310" y="143" fill="#{TEXT}" font-family="Segoe UI,Arial,sans-serif" font-size="15">⑂ {forks}</text>
  <text x="410" y="143" fill="#{TEXT}" font-family="Segoe UI,Arial,sans-serif" font-size="15">{esc(license_name)}</text>

  <text x="54" y="180" fill="#999999" font-family="Segoe UI,Arial,sans-serif" font-size="13">Updated {esc(updated)}</text>
  <text x="786" y="180" text-anchor="end" fill="#{ACCENT}" font-family="Segoe UI,Arial,sans-serif" font-size="13">github.com</text>
</svg>
'''


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for url in PROJECTS:
        full_name = repo_name(url)
        owner, name = full_name.split("/", 1)
        repo = fetch_repo(full_name)
        filename = name.lower().replace("_", "-").replace(" ", "-") + ".svg"
        path = OUTPUT_DIR / filename
        path.write_text(make_card(repo), encoding="utf-8")
        print(f"Generated: {path} <- {owner}/{name}")


if __name__ == "__main__":
    main()
