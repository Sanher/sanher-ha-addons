#!/usr/bin/env python3
import json
import os
import re
import sys
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ADDONS = [
    {
        "name": "agent_runner",
        "repo": "Sanher/Agent_runner",
        "config": Path("agent_runner/config.yaml"),
        "dockerfile": Path("agent_runner/Dockerfile"),
        "changelog": Path("agent_runner/CHANGELOG.md"),
    },
    {
        "name": "17track_app",
        "repo": "sanher/17Track_app",
        "config": Path("17track_app/config.yaml"),
        "dockerfile": Path("17track_app/Dockerfile"),
        "changelog": Path("17track_app/CHANGELOG.md"),
    },
]

TAG_RE = re.compile(r"^v?(\d+)\.(\d+)(?:\.(\d+))?$")


@dataclass(order=True)
class Version:
    major: int
    minor: int
    patch: int
    text: str = field(compare=False)


@dataclass
class UpstreamInfo:
    version: Version
    tag_name: str
    commit_sha: str
    commit_message: str


def parse_version(tag: str) -> Optional[Version]:
    match = TAG_RE.fullmatch(tag.strip())
    if not match:
        return None

    major = int(match.group(1))
    minor = int(match.group(2))
    patch_raw = match.group(3)
    patch = int(patch_raw) if patch_raw is not None else 0

    normalized = f"{major}.{minor}" if patch_raw is None else f"{major}.{minor}.{patch}"
    return Version(major=major, minor=minor, patch=patch, text=normalized)


def github_get_json(url: str) -> Any:
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "sanher-ha-addons-version-sync",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def normalize_commit_subject(message: str) -> str:
    subject = message.splitlines()[0].strip()
    subject = " ".join(subject.split())
    subject = subject.replace("`", "'")
    return subject[:180] if len(subject) > 180 else subject


def fetch_latest_upstream(repo: str) -> UpstreamInfo:
    tags_payload = github_get_json(f"https://api.github.com/repos/{repo}/tags?per_page=100")

    candidates: List[Tuple[Version, Dict[str, Any]]] = []
    for item in tags_payload:
        tag_name = item.get("name", "")
        version = parse_version(tag_name)
        if version is not None:
            candidates.append((version, item))

    if not candidates:
        raise RuntimeError(f"No se encontraron tags de versión válidas en {repo}")

    version, tag_item = max(candidates, key=lambda item: item[0])
    commit_sha = tag_item.get("commit", {}).get("sha")
    if not commit_sha:
        raise RuntimeError(f"No se encontró commit SHA para tag en {repo}")

    commit_payload = github_get_json(f"https://api.github.com/repos/{repo}/commits/{commit_sha}")
    raw_message = commit_payload.get("commit", {}).get("message", "")
    commit_message = normalize_commit_subject(raw_message) or "Sin mensaje de commit"

    return UpstreamInfo(
        version=version,
        tag_name=tag_item.get("name", f"v{version.text}"),
        commit_sha=commit_sha,
        commit_message=commit_message,
    )


def replace_once(pattern: str, repl: str, content: str, path: Path) -> str:
    result, count = re.subn(pattern, repl, content, count=1, flags=re.MULTILINE)
    if count == 0:
        raise RuntimeError(f"No se pudo actualizar patrón en {path}")
    return result


def update_changelog(path: Path, version_text: str, repo: str, tag_name: str, commit_message: str) -> bool:
    content = path.read_text(encoding="utf-8")
    section_title = f"## {version_text}"

    if re.search(rf"^{re.escape(section_title)}\s*$", content, flags=re.MULTILINE):
        return False

    line = f"- Sync upstream `{repo}` ({tag_name}): {commit_message}."
    entry = f"{section_title}\n\n{line}\n\n"

    if content.startswith("# Changelog"):
        lines = content.splitlines(keepends=True)
        rest = "".join(lines[1:]).lstrip("\n")
        new_content = f"# Changelog\n\n{entry}{rest}"
    else:
        new_content = f"{entry}{content}"

    path.write_text(new_content, encoding="utf-8")
    return True


def update_addon(addon: Dict[str, Any]) -> Tuple[bool, str, Version]:
    upstream = fetch_latest_upstream(addon["repo"])
    latest = upstream.version

    config_path = addon["config"]
    docker_path = addon["dockerfile"]
    changelog_path = addon["changelog"]

    config_content = config_path.read_text(encoding="utf-8")
    docker_content = docker_path.read_text(encoding="utf-8")

    config_match = re.search(r'^version:\s+"([^"]+)"\s*$', config_content, flags=re.MULTILINE)
    docker_match = re.search(r"^ARG APP_REF=(.+)$", docker_content, flags=re.MULTILINE)
    if not config_match or not docker_match:
        raise RuntimeError(f"No se pudo leer versión actual de {addon['name']}")

    current_config = config_match.group(1)
    current_ref = docker_match.group(1).strip()
    current_ref_no_v = current_ref[1:] if current_ref.startswith("v") else current_ref
    target_ref = f"v{latest.text}"

    changed = False
    if current_config != latest.text:
        config_content = replace_once(
            r'^version:\s+"[^"]+"\s*$',
            f'version: "{latest.text}"',
            config_content,
            config_path,
        )
        changed = True

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
        update_changelog(
            path=changelog_path,
            version_text=latest.text,
            repo=addon["repo"],
            tag_name=upstream.tag_name,
            commit_message=upstream.commit_message,
        )

    return changed, addon["name"], latest


def write_output(name: str, value: str) -> None:
    output_path = os.getenv("GITHUB_OUTPUT")
    if not output_path:
        return
    with open(output_path, "a", encoding="utf-8") as output_file:
        output_file.write(f"{name}={value}\n")


def main() -> int:
    changes: List[Tuple[str, Version]] = []

    for addon in ADDONS:
        changed, addon_name, latest = update_addon(addon)
        if changed:
            changes.append((addon_name, latest))

    if not changes:
        print("Sin cambios de versión")
        write_output("changed", "false")
        return 0

    highest = max(version for _, version in changes)
    details = ", ".join(f"{name}={version.text}" for name, version in changes)
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
