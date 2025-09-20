from swarms_tools.devs.github import get_user_info, get_repo_details, list_repo_issues

# Get user information
username = "octocat"
user_info = get_user_info(username)
print(f"User info for {username}:")
print(f"  Name: {user_info.get('name', 'N/A')}")
print(f"  Public repos: {user_info.get('public_repos', 'N/A')}")
print(f"  Followers: {user_info.get('followers', 'N/A')}")

# Get repository details
owner = "microsoft"
repo = "vscode"
repo_details = get_repo_details(owner, repo)
print(f"\nRepository: {repo_details.get('full_name', 'N/A')}")
print(f"Description: {repo_details.get('description', 'N/A')}")
print(f"Stars: {repo_details.get('stargazers_count', 'N/A')}")
print(f"Language: {repo_details.get('language', 'N/A')}")

# List open issues
issues = list_repo_issues(owner, repo, state="open")
print(f"\nFound {len(issues)} open issues")
for issue in issues[:3]:  # Show first 3 issues
    print(f"  - Issue #{issue.get('number', 'N/A')}: {issue.get('title', 'N/A')}")
    print(f"    State: {issue.get('state', 'N/A')}")
    print(f"    Created: {issue.get('created_at', 'N/A')}")
