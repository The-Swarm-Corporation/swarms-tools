"""
GitHub API Example

This example demonstrates how to use the GitHub API tools to interact with GitHub repositories,
manage issues, pull requests, and collaborate with team members.

Requirements:
- GITHUB_TOKEN environment variable must be set
- Install required dependencies: httpx, loguru, python-dotenv

Usage:
    python github_example.py
"""

import os
from dotenv import load_dotenv
from loguru import logger
from swarms_tools.devs.github import (
    get_user_info,
    list_repo_issues,
    create_issue,
    list_open_prs,
    get_repo_details,
    close_issue,
    create_pull_request,
    merge_pull_request,
    list_repo_collaborators,
    add_repo_collaborator
)

# Load environment variables
load_dotenv()


def main():
    """
    Main function demonstrating GitHub API usage.
    """
    logger.info("Starting GitHub API example...")
    
    # Check if GitHub token is available
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        logger.error("GITHUB_TOKEN not found in environment variables")
        logger.info("Please set your GitHub token in the .env file")
        logger.info("You can create a token at: https://github.com/settings/tokens")
        return
    
    # Example repository (you can change these to your own repos)
    owner = "microsoft"  # Example owner
    repo = "vscode"      # Example repository
    
    try:
        # Example 1: Get user information
        logger.info("Example 1: Getting user information")
        username = "octocat"  # GitHub's example user
        user_info = get_user_info(username)
        logger.info(f"User info for {username}:")
        logger.info(f"  Name: {user_info.get('name', 'N/A')}")
        logger.info(f"  Public repos: {user_info.get('public_repos', 'N/A')}")
        logger.info(f"  Followers: {user_info.get('followers', 'N/A')}")
        logger.info(f"  Following: {user_info.get('following', 'N/A')}")
        
        # Example 2: Get repository details
        logger.info("Example 2: Getting repository details")
        repo_details = get_repo_details(owner, repo)
        logger.info(f"Repository: {repo_details.get('full_name', 'N/A')}")
        logger.info(f"Description: {repo_details.get('description', 'N/A')}")
        logger.info(f"Stars: {repo_details.get('stargazers_count', 'N/A')}")
        logger.info(f"Forks: {repo_details.get('forks_count', 'N/A')}")
        logger.info(f"Language: {repo_details.get('language', 'N/A')}")
        logger.info(f"Open issues: {repo_details.get('open_issues_count', 'N/A')}")
        
        # Example 3: List open issues
        logger.info("Example 3: Listing open issues")
        issues = list_repo_issues(owner, repo, state="open")
        logger.info(f"Found {len(issues)} open issues")
        for issue in issues[:3]:  # Show first 3 issues
            logger.info(f"  - Issue #{issue.get('number', 'N/A')}: {issue.get('title', 'N/A')}")
            logger.info(f"    State: {issue.get('state', 'N/A')}")
            logger.info(f"    Created: {issue.get('created_at', 'N/A')}")
        
        # Example 4: List open pull requests
        logger.info("Example 4: Listing open pull requests")
        prs = list_open_prs(owner, repo)
        logger.info(f"Found {len(prs)} open pull requests")
        for pr in prs[:3]:  # Show first 3 PRs
            logger.info(f"  - PR #{pr.get('number', 'N/A')}: {pr.get('title', 'N/A')}")
            logger.info(f"    State: {pr.get('state', 'N/A')}")
            logger.info(f"    Head: {pr.get('head', {}).get('ref', 'N/A')}")
            logger.info(f"    Base: {pr.get('base', {}).get('ref', 'N/A')}")
        
        # Example 5: List collaborators
        logger.info("Example 5: Listing repository collaborators")
        try:
            collaborators = list_repo_collaborators(owner, repo)
            logger.info(f"Found {len(collaborators)} collaborators")
            for collab in collaborators[:3]:  # Show first 3 collaborators
                permissions = collab.get('permissions', {})
                logger.info(f"  - {collab.get('login', 'N/A')}")
                logger.info(f"    Admin: {permissions.get('admin', False)}")
                logger.info(f"    Push: {permissions.get('push', False)}")
                logger.info(f"    Pull: {permissions.get('pull', False)}")
        except Exception as e:
            logger.warning(f"Could not fetch collaborators (may require admin access): {e}")
        
        # Example 6: List closed issues
        logger.info("Example 6: Listing closed issues")
        closed_issues = list_repo_issues(owner, repo, state="closed")
        logger.info(f"Found {len(closed_issues)} closed issues")
        for issue in closed_issues[:2]:  # Show first 2 closed issues
            logger.info(f"  - Issue #{issue.get('number', 'N/A')}: {issue.get('title', 'N/A')}")
            logger.info(f"    Closed: {issue.get('closed_at', 'N/A')}")
        
        # Example 7: List all issues
        logger.info("Example 7: Listing all issues")
        all_issues = list_repo_issues(owner, repo, state="all")
        logger.info(f"Found {len(all_issues)} total issues")
        
        # Example 8: Create an issue (commented out to avoid spam)
        logger.info("Example 8: Creating an issue (commented out)")
        logger.info("To test issue creation, uncomment the following code:")
        logger.info("# issue_title = 'Example Issue from GitHub API'")
        logger.info("# issue_body = 'This is an example issue created using the GitHub API tool.'")
        logger.info("# issue_labels = ['example', 'api']")
        logger.info("# new_issue = create_issue(owner, repo, issue_title, issue_body, issue_labels)")
        logger.info("# logger.info(f'Created issue: {new_issue.get('html_url', 'N/A')}')")
        
        # Example 9: Create a pull request (commented out to avoid spam)
        logger.info("Example 9: Creating a pull request (commented out)")
        logger.info("To test PR creation, uncomment the following code:")
        logger.info("# pr_title = 'Example PR from GitHub API'")
        logger.info("# pr_body = 'This is an example pull request created using the GitHub API tool.'")
        logger.info("# head_branch = 'feature-branch'")
        logger.info("# base_branch = 'main'")
        logger.info("# new_pr = create_pull_request(owner, repo, pr_title, head_branch, base_branch, pr_body)")
        logger.info("# logger.info(f'Created PR: {new_pr.get('html_url', 'N/A')}')")
        
        # Example 10: Close an issue (commented out to avoid spam)
        logger.info("Example 10: Closing an issue (commented out)")
        logger.info("To test issue closing, uncomment the following code:")
        logger.info("# issue_number = 12345  # Replace with actual issue number")
        logger.info("# closed_issue = close_issue(owner, repo, issue_number)")
        logger.info("# logger.info(f'Closed issue: {closed_issue.get('html_url', 'N/A')}')")
        
        logger.info("GitHub API examples completed successfully!")
        logger.info("Note: Write operations (create, close, merge) are commented out to avoid spam")
        
    except Exception as e:
        logger.error(f"Error with GitHub API: {e}")
        logger.info("Make sure your GitHub token has the necessary permissions")
        logger.info("Required scopes: repo (for private repos), public_repo (for public repos)")


if __name__ == "__main__":
    main()
