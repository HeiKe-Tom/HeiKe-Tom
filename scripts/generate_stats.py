#!/usr/bin/env python3
"""Generate a static GitHub profile statistics SVG without Vercel."""

from __future__ import annotations

import json
import os
from pathlib import Path
from urllib.request import Request, urlopen

OUTPUT_DIR = Path("assets/stats")
BG = "17150d"
TITLE = "a8c7fa"
TEXT = "e5e5e5"
BORDER = "555555"


def github_api(path: str):
    request = Request(
        f"https://api.github.com{path}",
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
    return (
        str(value or "")
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def main() -> None:
    profile = github_api("/users/HeiKe-Tom")
    repos = github_api("/users/HeiKe-Tom/repos?per_page=100&sort=updated")

    public_repos = profile.get("public_repos", 0)
    followers = profile.get("followers", 0)
    following = profile.get("following", 0)
    stars = sum(repo.get("stargazers_count", 0) for repo in repos)
    forks = sum(repo.get("forks_count", 0) for repo in repos)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="840" height="220" viewBox="0 0 840 220" role="img" aria-label="GitHub statistics for HeiKe-Tom">
  <rect x="1" y="1" width="838" height="218" rx="16" fill="#{BG}" stroke="#{BORDER}" stroke-width="2"/>
  <text x="40" y="52" fill="#{TITLE}" font-family="Segoe UI,Arial,sans-serif" font-size="25" font-weight="700">GitHub Statistics</text>
  <text x="40" y="78" fill="#{TEXT}" font-family="Segoe UI,Arial,sans-serif" font-size="15">HeiKe-Tom</text>

  <text x="70" y="125" fill="#{TITLE}" font-family="Segoe UI,Arial,sans-serif" font-size="28" font-weight="700">{public_repos}</text>
  <text x="70" y="149" fill="#{TEXT}" font-family="Segoe UI,Arial,sans-serif" font-size="13">Repositories</text>

  <text x="245" y="125" fill="#{TITLE}" font-family="Segoe UI,Arial,sans-serif" font-size="28" font-weight="700">{stars}</text>
  <text x="245" y="149" fill="#{TEXT}" font-family="Segoe UI,Arial,sans-serif" font-size="13">Stars received</text>

  <text x="420" y="125" fill="#{TITLE}" font-family="Segoe UI,Arial,sans-serif" font-size="28" font-weight="700">{forks}</text>
  <text x="420" y="149" fill="#{TEXT}" font-family="Segoe UI,Arial,sans-serif" font-size="13">Forks</text>

  <text x="580" y="125" fill="#{TITLE}" font-family="Segoe UI,Arial,sans-serif" font-size="28" font-weight="700">{followers}</text>
  <text x="580" y="149" fill="#{TEXT}" font-family="Segoe UI,Arial,sans-serif" font-size="13">Followers</text>

  <text x="720" y="125" fill="#{TITLE}" font-family="Segoe UI,Arial,sans-serif" font-size="28" font-weight="700">{following}</text>
  <text x="720" y="149" fill="#{TEXT}" font-family="Segoe UI,Arial,sans-serif" font-size="13">Following</text>

  <text x="40" y="190" fill="#999999" font-family="Segoe UI,Arial,sans-serif" font-size="12">Generated automatically by GitHub Actions · No Vercel API</text>
</svg>
'''
    (OUTPUT_DIR / "github-stats.svg").write_text(svg, encoding="utf-8")
    print("Generated assets/stats/github-stats.svg")


if __name__ == "__main__":
    main()
