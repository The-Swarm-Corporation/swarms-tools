from swarms_tools.devs.github import (
    get_user_info, get_repo_details, list_repo_issues, create_issue,
    list_open_prs, close_issue, create_pull_request, merge_pull_request,
    list_repo_collaborators, add_repo_collaborator
)

# Test that all functions exist and are callable
assert callable(get_user_info)
assert callable(get_repo_details)
assert callable(list_repo_issues)
assert callable(create_issue)
assert callable(list_open_prs)
assert callable(close_issue)
assert callable(create_pull_request)
assert callable(merge_pull_request)
assert callable(list_repo_collaborators)
assert callable(add_repo_collaborator)

# Test user info function with real API call
username = "octocat"
user_info = get_user_info(username)
assert user_info is not None
assert isinstance(user_info, dict)
assert 'login' in user_info
assert user_info['login'] == username
assert 'public_repos' in user_info
assert 'followers' in user_info

# Test repository details function
owner = "microsoft"
repo = "vscode"
repo_details = get_repo_details(owner, repo)
assert repo_details is not None
assert isinstance(repo_details, dict)
assert 'full_name' in repo_details
assert repo_details['full_name'] == f"{owner}/{repo}"
assert 'stargazers_count' in repo_details
assert 'language' in repo_details

# Test issues listing function
issues = list_repo_issues(owner, repo, state="open")
assert issues is not None
assert isinstance(issues, list)
assert len(issues) >= 0  # Can be empty but should be a list

# Test that each issue has required fields
if issues:
    issue = issues[0]
    assert isinstance(issue, dict)
    assert 'number' in issue
    assert 'title' in issue
    assert 'state' in issue
    assert 'created_at' in issue

# Test pull requests listing function
prs = list_open_prs(owner, repo)
assert prs is not None
assert isinstance(prs, list)
assert len(prs) >= 0  # Can be empty but should be a list

# Test that each PR has required fields
if prs:
    pr = prs[0]
    assert isinstance(pr, dict)
    assert 'number' in pr
    assert 'title' in pr
    assert 'state' in pr
    assert 'head' in pr
    assert 'base' in pr
