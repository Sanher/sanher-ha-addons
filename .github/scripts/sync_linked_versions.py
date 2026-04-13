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
    {
        "name": "learn-languages",
        "repo": "Sanher/learn-languages",
        "config": Path("learn-languages/config.yaml"),
        "dockerfile": Path("learn-languages/Dockerfile"),
        "changelog": Path("learn-languages/CHANGELOG.md"),
    },
    {
        "name": "rustdesk_server",
        "repo": "Sanher/Rustdesk_wrapper",
        "config": Path("rustdesk_server/config.yaml"),
        "dockerfile": Path("rustdesk_server/Dockerfile"),
        "changelog": Path("rustdesk_server/CHANGELOG.md"),
    },
    {
        "name": "happy_server",
        "repo": "Sanher/Happy_server",
        "config": Path("happy_server/config.yaml"),
        "dockerfile": Path("happy_server/Dockerfile"),
        "changelog": Path("happy_server/CHANGELOG.md"),
    },
    {
        "name": "omnitools",
        "repo": "Sanher/Omnitools",
        "config": Path("omnitools/config.yaml"),
        "dockerfile": Path("omnitools/Dockerfile"),
        "changelog": Path("omnitools/CHANGELOG.md"),
        "sync_docker_ref": False,
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
            "User-Agent": "ha-addons-version-sync",
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


def fetch_tagged_upstream(
    repo: str,
    tag_name: str,
    commit_sha: Optional[str] = None,
    commit_message: Optional[str] = None,
) -> UpstreamInfo:
    version = parse_version(tag_name)
    if version is None:
        raise RuntimeError(f"Tag no válida para sincronización en {repo}: {tag_name}")

    resolved_sha = commit_sha
    resolved_message = normalize_commit_subject(commit_message or "")

    if not resolved_sha:
        tag_payload = github_get_json(f"https://api.github.com/repos/{repo}/tags?per_page=100")
        tag_item = next((item for item in tag_payload if item.get("name") == tag_name), None)
        if not tag_item:
            raise RuntimeError(f"No se encontró la tag {tag_name} en {repo}")
        resolved_sha = tag_item.get("commit", {}).get("sha")

    if not resolved_sha:
        raise RuntimeError(f"No se pudo resolver el commit SHA de {tag_name} en {repo}")

    if not resolved_message:
        commit_payload = github_get_json(f"https://api.github.com/repos/{repo}/commits/{resolved_sha}")
        raw_message = commit_payload.get("commit", {}).get("message", "")
        resolved_message = normalize_commit_subject(raw_message) or "Sin mensaje de commit"

    return UpstreamInfo(
        version=version,
        tag_name=tag_name,
        commit_sha=resolved_sha,
        commit_message=resolved_message,
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


def update_addon(addon: Dict[str, Any], upstream: Optional[UpstreamInfo] = None) -> Tuple[bool, str, Version]:
    upstream = upstream or fetch_latest_upstream(addon["repo"])
    latest = upstream.version

    config_path = addon["config"]
    docker_path = addon.get("dockerfile")
    changelog_path = addon["changelog"]

    config_content = config_path.read_text(encoding="utf-8")
    docker_content = docker_path.read_text(encoding="utf-8") if docker_path else None
    changed = False

    config_match = re.search(r'^version:\s+"([^"]+)"\s*$', config_content, flags=re.MULTILINE)
    docker_match = re.search(r"^ARG APP_REF=(.+)$", docker_content, flags=re.MULTILINE) if docker_content else None
    if not config_match:
        raise RuntimeError(f"No se pudo leer versión actual de {addon['name']}")
    if docker_path and not docker_match:
        raise RuntimeError(f"No se pudo leer ARG APP_REF de {addon['name']}")

    current_config = config_match.group(1)
    current_ref = docker_match.group(1).strip() if docker_match else ""
    current_ref_no_v = current_ref[1:] if current_ref.startswith("v") else current_ref
    target_ref = upstream.tag_name

    if addon.get("sync_config_version", True) and current_config != latest.text:
        config_content = replace_once(
            r'^version:\s+"[^"]+"\s*$',
            f'version: "{latest.text}"',
            config_content,
            config_path,
        )
        changed = True

    if addon.get("sync_docker_ref", True):
        if current_ref_no_v != latest.text or current_ref != target_ref:
            docker_content = replace_once(
                r"^ARG APP_REF=.+$",
                f"ARG APP_REF={target_ref}",
                docker_content,
                docker_path,
            )
            changed = True

    if changed:
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(config_content, encoding="utf-8")
        if docker_path and docker_content is not None:
            docker_path.parent.mkdir(parents=True, exist_ok=True)
            docker_path.write_text(docker_content, encoding="utf-8")
        update_changelog(
            path=changelog_path,
            version_text=latest.text,
            repo=addon["repo"],
            tag_name=upstream.tag_name,
            commit_message=upstream.commit_message,
        )

    return changed, addon["name"], latest


def get_dispatch_target() -> Optional[Dict[str, str]]:
    repo = os.getenv("SYNC_TARGET_REPO", "").strip()
    tag = os.getenv("SYNC_TARGET_TAG", "").strip()
    sha = os.getenv("SYNC_TARGET_SHA", "").strip()
    commit_message = os.getenv("SYNC_TARGET_COMMIT_MESSAGE", "").strip()

    if not repo and not tag:
        return None
    if not repo or not tag:
        raise RuntimeError("SYNC_TARGET_REPO y SYNC_TARGET_TAG deben viajar juntos")

    return {
        "repo": repo,
        "tag": tag,
        "sha": sha,
        "commit_message": commit_message,
    }


def find_addon_by_repo(repo: str) -> Dict[str, Any]:
    repo_key = repo.lower()
    for addon in ADDONS:
        if addon["repo"].lower() == repo_key:
            return addon
    raise RuntimeError(f"No se encontró addon configurado para repo {repo}")


def write_output(name: str, value: str) -> None:
    output_path = os.getenv("GITHUB_OUTPUT")
    if not output_path:
        return
    with open(output_path, "a", encoding="utf-8") as output_file:
        output_file.write(f"{name}={value}\n")


def main() -> int:
    changes: List[Tuple[str, Version]] = []
    dispatch_target = get_dispatch_target()

    if dispatch_target:
        addon = find_addon_by_repo(dispatch_target["repo"])
        upstream = fetch_tagged_upstream(
            repo=dispatch_target["repo"],
            tag_name=dispatch_target["tag"],
            commit_sha=dispatch_target["sha"] or None,
            commit_message=dispatch_target["commit_message"] or None,
        )
        changed, addon_name, latest = update_addon(addon, upstream=upstream)
        if changed:
            changes.append((addon_name, latest))
    else:
        for addon in ADDONS:
            if not addon.get("auto_sync", True):
                continue
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
