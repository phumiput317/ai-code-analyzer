import base64
import requests

from config import (
    GITHUB_REQUEST_TIMEOUT,
    GITHUB_TOKEN,
    MAX_FILE_SIZE,
    MAX_PROJECT_CHARS,
    MAX_REPOSITORY_FILES,
    OWNER,
    REPO,
)
from logger import logger


def _request_headers():
    headers = {"Accept": "application/vnd.github+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    return headers


def get_repository_files(owner=None, repo=None, path=""):
    owner = owner or OWNER
    repo = repo or REPO

    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"

    try:
        response = requests.get(
            url,
            headers=_request_headers(),
            timeout=GITHUB_REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        logger.error("GitHub request timed out: %s", url)
        return []
    except requests.exceptions.RequestException as e:
        logger.error(f"GitHub API error: {e}")
        return []


def read_github_file(file_info):
    try:
        encoded_content = file_info["content"]
        content = base64.b64decode(encoded_content).decode("utf-8", errors="ignore")
        return content
    except Exception as e:
        print("Cannot read file:", e)
        return ""


def collect_repository_code(owner=None, repo=None, path=""):
    owner = owner or OWNER
    repo = repo or REPO

    allowed_extensions = (
        ".py",
        ".js",
        ".ts",
        ".tsx",
        ".jsx",
        ".java",
        ".go",
        ".html",
        ".css",
        ".json",
    )

    collected = []
    total_chars = 0

    def collect(current_path):
        nonlocal total_chars

        if len(collected) >= MAX_REPOSITORY_FILES:
            return

        for item in get_repository_files(owner, repo, current_path):
            if len(collected) >= MAX_REPOSITORY_FILES:
                logger.warning("Repository file limit reached.")
                return

            if item.get("type") == "dir":
                collect(item.get("path", ""))
                continue

            if item.get("type") != "file" or not item.get("name", "").endswith(
                allowed_extensions
            ):
                continue

            file_size = item.get("size", 0)
            if file_size > MAX_FILE_SIZE:
                logger.warning("Skipping oversized file: %s", item.get("path"))
                continue

            logger.info("Reading file: %s", item.get("path"))
            try:
                response = requests.get(
                    item["url"],
                    headers=_request_headers(),
                    timeout=GITHUB_REQUEST_TIMEOUT,
                )
                response.raise_for_status()
                code = read_github_file(response.json())
            except requests.exceptions.RequestException as error:
                logger.error("Cannot read GitHub file %s: %s", item.get("path"), error)
                continue

            remaining_chars = MAX_PROJECT_CHARS - total_chars
            if not code or remaining_chars <= 0:
                logger.warning("Project character limit reached.")
                return

            code = code[:remaining_chars]
            collected.append({"path": item["path"], "code": code})
            total_chars += len(code)

    collect(path)
    return collected


def get_recent_commits(owner=None, repo=None):
    owner = owner or OWNER
    repo = repo or REPO
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"

    try:
        response = requests.get(
            url,
            headers=_request_headers(),
            timeout=GITHUB_REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Cannot get commits: {e}")
        return []


def get_changed_files_from_latest_commit(owner=None, repo=None):
    owner = owner or OWNER
    repo = repo or REPO
    commits = get_recent_commits(owner, repo)

    if not commits:
        return []

    latest_sha = commits[0]["sha"]
    url = f"https://api.github.com/repos/{owner}/{repo}/commits/{latest_sha}"

    try:
        response = requests.get(
            url,
            headers=_request_headers(),
            timeout=GITHUB_REQUEST_TIMEOUT,
        )
        response.raise_for_status()

        data = response.json()
        changed_files = []

        for file in data.get("files", []):
            changed_files.append({
                "filename": file.get("filename"),
                "status": file.get("status"),
                "additions": file.get("additions", 0),
                "deletions": file.get("deletions", 0),
                "changes": file.get("changes", 0),
                "patch": file.get("patch", "")
            })

        return changed_files
    except requests.exceptions.RequestException as e:
        logger.error(f"Cannot get changed files: {e}")
        return []