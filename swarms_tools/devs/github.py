import os
import httpx
from dotenv import load_dotenv
from loguru import logger
from typing import Any, Dict, List, Optional

# Load environment variables
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_API_URL = "https://api.github.com"

if not GITHUB_TOKEN:
    logger.error("Missing GITHUB_TOKEN in .env file")
    raise ValueError(
        "GITHUB_TOKEN not found in environment variables"
    )

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}


def get_user_info(username: str) -> Dict[str, Any]:
    """
    Fetch information about a GitHub user.

    Args:
        username (str): GitHub username.

    Returns:
        Dict[str, Any]: User information.
    """
    url = f"{GITHUB_API_URL}/users/{username}"
    logger.info(f"Fetching user info for {username}")
    response = httpx.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def list_repo_issues(
    owner: str, repo: str, state: str = "open"
) -> List[Dict[str, Any]]:
    """
    List issues for a repository.

    Args:
        owner (str): Repository owner.
        repo (str): Repository name.
        state (str): Issue state (open, closed, all). Defaults to "open".

    Returns:
        List[Dict[str, Any]]: List of issues.
    """
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/issues"
    params = {"state": state}
    logger.info(f"Listing {state} issues for {owner}/{repo}")
    response = httpx.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def create_issue(
    owner: str,
    repo: str,
    title: str,
    body: Optional[str] = None,
    labels: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Create an issue in a repository.

    Args:
        owner (str): Repository owner.
        repo (str): Repository name.
        title (str): Issue title.
        body (Optional[str]): Issue description. Defaults to None.
        labels (Optional[List[str]]): List of labels for the issue. Defaults to None.

    Returns:
        Dict[str, Any]: Created issue details.
    """
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/issues"
    payload = {"title": title, "body": body, "labels": labels}
    logger.info(
        f"Creating issue in {owner}/{repo} with title: {title}"
    )
    response = httpx.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()


def list_open_prs(owner: str, repo: str) -> List[Dict[str, Any]]:
    """
    List open pull requests for a repository.

    Args:
        owner (str): Repository owner.
        repo (str): Repository name.

    Returns:
        List[Dict[str, Any]]: List of open pull requests.
    """
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/pulls"
    logger.info(f"Listing open pull requests for {owner}/{repo}")
    response = httpx.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def get_repo_details(owner: str, repo: str) -> Dict[str, Any]:
    """
    Get details about a repository.

    Args:
        owner (str): Repository owner.
        repo (str): Repository name.

    Returns:
        Dict[str, Any]: Repository details.
    """
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}"
    logger.info(f"Fetching details for repository {owner}/{repo}")
    response = httpx.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def close_issue(
    owner: str, repo: str, issue_number: int
) -> Dict[str, Any]:
    """
    Close an issue in a repository.

    Args:
        owner (str): Repository owner.
        repo (str): Repository name.
        issue_number (int): Issue number.

    Returns:
        Dict[str, Any]: Updated issue details.
    """
    url = (
        f"{GITHUB_API_URL}/repos/{owner}/{repo}/issues/{issue_number}"
    )
    payload = {"state": "closed"}
    logger.info(f"Closing issue #{issue_number} in {owner}/{repo}")
    response = httpx.patch(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()


def create_pull_request(
    owner: str,
    repo: str,
    title: str,
    head: str,
    base: str,
    body: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Create a pull request in a repository.

    Args:
        owner (str): Repository owner.
        repo (str): Repository name.
        title (str): Pull request title.
        head (str): Branch where changes are implemented.
        base (str): Branch into which the pull request will be merged.
        body (Optional[str]): Pull request description. Defaults to None.

    Returns:
        Dict[str, Any]: Created pull request details.
    """
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/pulls"
    payload = {
        "title": title,
        "head": head,
        "base": base,
        "body": body,
    }
    logger.info(
        f"Creating pull request in {owner}/{repo} from {head} to {base} with title: {title}"
    )
    response = httpx.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()


def merge_pull_request(
    owner: str, repo: str, pr_number: int
) -> Dict[str, Any]:
    """
    Merge a pull request in a repository.

    Args:
        owner (str): Repository owner.
        repo (str): Repository name.
        pr_number (int): Pull request number.

    Returns:
        Dict[str, Any]: Merged pull request details.
    """
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/pulls/{pr_number}/merge"
    logger.info(
        f"Merging pull request #{pr_number} in {owner}/{repo}"
    )
    response = httpx.put(url, headers=headers)
    response.raise_for_status()
    return response.json()


def list_repo_collaborators(
    owner: str, repo: str
) -> List[Dict[str, Any]]:
    """
    List collaborators for a repository.

    Args:
        owner (str): Repository owner.
        repo (str): Repository name.

    Returns:
        List[Dict[str, Any]]: List of collaborators.
    """
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/collaborators"
    logger.info(f"Listing collaborators for {owner}/{repo}")
    response = httpx.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def add_repo_collaborator(
    owner: str, repo: str, username: str, permission: str = "push"
) -> Dict[str, Any]:
    """
    Add a collaborator to a repository.

    Args:
        owner (str): Repository owner.
        repo (str): Repository name.
        username (str): Collaborator's GitHub username.
        permission (str): Permission level (pull, push, admin). Defaults to "push".

    Returns:
        Dict[str, Any]: Response details.
    """
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/collaborators/{username}"
    payload = {"permission": permission}
    logger.info(
        f"Adding {username} as a collaborator to {owner}/{repo} with permission: {permission}"
    )
    response = httpx.put(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()
