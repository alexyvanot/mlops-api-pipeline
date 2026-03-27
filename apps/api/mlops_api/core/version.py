import os
import subprocess
from dataclasses import dataclass


@dataclass(frozen=True)
class VersionInfo:
    app_version: str
    git_commit: str
    git_branch: str


def _read_git_value(args: list[str]) -> str | None:
    try:
        completed = subprocess.run(
            ["git", *args],
            check=True,
            capture_output=True,
            text=True,
            timeout=2,
        )
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return None

    value = completed.stdout.strip()
    return value or None


def get_version_info(app_version: str) -> VersionInfo:
    git_commit = (
        os.getenv("APP_GIT_COMMIT")
        or os.getenv("GITHUB_SHA")
        or _read_git_value(["rev-parse", "--short", "HEAD"])
        or "unknown"
    )
    git_branch = (
        os.getenv("APP_GIT_BRANCH")
        or os.getenv("GITHUB_REF_NAME")
        or _read_git_value(["rev-parse", "--abbrev-ref", "HEAD"])
        or "unknown"
    )

    return VersionInfo(
        app_version=app_version,
        git_commit=git_commit,
        git_branch=git_branch,
    )
