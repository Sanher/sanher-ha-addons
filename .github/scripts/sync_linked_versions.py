#!/usr/bin/env python3
import json
import os
import re
import sys
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple

ADDONS = [
    {
        "name": "agent_runner",
        "repo": "Sanher/Agent_runner",
        "config": Path("agent_runner/config.yaml"),
        "dockerfile": Path("agent_runner/Dockerfile"),
    },
    {
        "name": "17track_app",
        "repo": "sanher/17Track_app",
        "config": Path("17track_app/config.yaml"),
        "dockerfile": Path("17track_app/Dockerfile"),
    },
]

TAG_RE = re.compile(r"^v?(\d+)\.(\d+)(?:\.(\d+))?$")


@dataclass(order=True)
class Version:
    major: int
    minor: int
    patch: int
    text: str


def parse_version(tag: str) -> Optional[Version]:
    match = TAG_RE.fullmatch(tag.strip())
    if not match:
        return None

    major = int(match.group(1))
    minor = int(match.group(2))
    patch_raw = match.group(3)
    patch = int(patch_raw) if patch_raw is not None else 0

    if patch_raw is None:
        normalized = f"{major}.{minor}"
    else:
        normalized = f"{major}.{minor}.{patch}"

    return Version(major=major, minor=minor, patch=patch, text=normalized)


def fetch_latest_tag(repo: str) -> Version:
    url = f"https://api.github.com/repos/{repo}/tags?per_page=100"
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "sanher-ha-addons-version-sync",
        },
    )

    with urllib.request.urlopen(req, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))

    versions: List[Version] = []
    for item in payload:
        name = item.get("name", "")
        parsed = parse_version(name)
        if parsed:
            versions.append(parsed)

    if not versions:
        raise RuntimeError(f"No se encontraron tags de versión válidas en {repo}")

    return max(versions)


def replace_once(pattern: str, repl: str, content: str, path: Path) -> str:
    result, count = re.subn(pattern, repl, content, count=1, flags=re.MULTILINE)
    if count == 0:
        raise RuntimeError(f"No se pudo actualizar patrón en {path}")
    return result


def update_addon(addon: dict) -> Tuple[bool, str, str]:
    latest = fetch_latest_tag(addon["repo"])

    config_path = addon["config"]
    docker_path = addon["dockerfile"]

    config_content = config_path.read_text(encoding="utf-8")
    docker_content = docker_path.read_text(encoding="utf-8")

    config_match = re.search(r'^version:\s+"([^"]+)"\s*$', config_content, flags=re.MULTILINE)
    docker_match = re.search(r"^ARG APP_REF=(.+)$", docker_content, flags=re.MULTILINE)

    if not config_match or not docker_match:
        raise RuntimeError(f"No se pudo leer versión actual de {addon['name']}")

    current_config = config_match.group(1)
    current_ref = docker_match.group(1).strip()
    current_ref_no_v = current_ref[1:] if current_ref.startswith("v") else current_ref

    changed = False

    if current_config != latest.text:
        config_content = replace_once(
            r'^version:\s+"[^"]+"\s*$',
            f'version: "{latest.text}"',
            config_content,
            config_path,
        )
        changed = True

    target_ref = f"v{latest.text}"
    if current_ref_no_v != latest.text or current_ref != target_ref:
        docker_content = replace_once(
            r"^ARG APP_REF=.+$",
            f"ARG APP_REF={target_ref}",
            docker_content,
            docker_path,
        )
        changed = True

    if changed:
        config_path.write_text(config_content, encoding="utf-8")
        docker_path.write_text(docker_content, encoding="utf-8")

    return changed, addon["name"], latest.text


def write_output(name: str, value: str) -> None:
    output_path = os.getenv("GITHUB_OUTPUT")
    if not output_path:
        return
    with open(output_path, "a", encoding="utf-8") as output_file:
        output_file.write(f"{name}={value}\n")


def main() -> int:
    changes: List[Tuple[str, str]] = []

    for addon in ADDONS:
        changed, addon_name, latest = update_addon(addon)
        if changed:
            changes.append((addon_name, latest))

    if not changes:
        print("Sin cambios de versión")
        write_output("changed", "false")
        return 0

    versions = [version for _, version in changes]
    highest = max(parse_version(v) for v in versions if parse_version(v) is not None)
    if highest is None:
        raise RuntimeError("No se pudo calcular versión para commit")

    details = ", ".join(f"{name}={version}" for name, version in changes)
    commit_msg = f"chore(version): bump to version {highest.text}"

    print(f"Cambios detectados: {details}")
    write_output("changed", "true")
    write_output("commit_message", commit_msg)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # pragma: no cover
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
