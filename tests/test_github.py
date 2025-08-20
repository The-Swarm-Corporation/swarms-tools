from loguru import logger


def test_get_user_info():
    try:
        from swarms_tools.devs.github import get_user_info

        username = "octocat"
        logger.info(
            f"Testing get_user_info with username: {username}"
        )
        result = get_user_info(username)
        assert "login" in result, "Key 'login' not found in result"
        logger.success("get_user_info test passed!")
    except Exception as e:
        logger.error(f"get_user_info test failed: {e}")


def test_list_repo_issues():
    try:
        from swarms_tools.devs.github import list_repo_issues

        owner, repo = "octocat", "Hello-World"
        logger.info(f"Testing list_repo_issues for {owner}/{repo}")
        result = list_repo_issues(owner, repo)
        assert isinstance(result, list), "Result is not a list"
        logger.success("list_repo_issues test passed!")
    except Exception as e:
        logger.error(f"list_repo_issues test failed: {e}")


def test_create_issue():
    try:
        from swarms_tools.devs.github import create_issue

        owner, repo = "octocat", "Hello-World"
        title = "Test Issue"
        logger.info(
            f"Testing create_issue for {owner}/{repo} with title: {title}"
        )
        result = create_issue(owner, repo, title, body="Test Body")
        assert (
            "title" in result and result["title"] == title
        ), "Issue creation failed"
        logger.success("create_issue test passed!")
    except Exception as e:
        logger.error(f"create_issue test failed: {e}")


def test_list_open_prs():
    try:
        from swarms_tools.devs.github import list_open_prs

        owner, repo = "octocat", "Hello-World"
        logger.info(f"Testing list_open_prs for {owner}/{repo}")
        result = list_open_prs(owner, repo)
        assert isinstance(result, list), "Result is not a list"
        logger.success("list_open_prs test passed!")
    except Exception as e:
        logger.error(f"list_open_prs test failed: {e}")


def test_get_repo_details():
    try:
        from swarms_tools.devs.github import get_repo_details

        owner, repo = "octocat", "Hello-World"
        logger.info(f"Testing get_repo_details for {owner}/{repo}")
        result = get_repo_details(owner, repo)
        assert (
            "name" in result and result["name"] == repo
        ), "Repository details mismatch"
        logger.success("get_repo_details test passed!")
    except Exception as e:
        logger.error(f"get_repo_details test failed: {e}")


def test_close_issue():
    try:
        from swarms_tools.devs.github import close_issue, create_issue

        owner, repo = "octocat", "Hello-World"
        title = "Test Issue to Close"
        logger.info(f"Testing close_issue for {owner}/{repo}")
        issue = create_issue(owner, repo, title, body="Test Body")
        issue_number = issue["number"]
        result = close_issue(owner, repo, issue_number)
        assert (
            result["state"] == "closed"
        ), "Issue not closed successfully"
        logger.success("close_issue test passed!")
    except Exception as e:
        logger.error(f"close_issue test failed: {e}")


def test_create_pull_request():
    try:
        from swarms_tools.devs.github import create_pull_request

        owner, repo = "octocat", "Hello-World"
        title, head, base = "Test PR", "feature-branch", "main"
        logger.info(f"Testing create_pull_request for {owner}/{repo}")
        result = create_pull_request(
            owner, repo, title, head, base, body="Test PR Body"
        )
        assert (
            "title" in result and result["title"] == title
        ), "Pull request creation failed"
        logger.success("create_pull_request test passed!")
    except Exception as e:
        logger.error(f"create_pull_request test failed: {e}")


def test_merge_pull_request():
    try:
        from swarms_tools.devs.github import (
            merge_pull_request,
            create_pull_request,
        )

        owner, repo = "octocat", "Hello-World"
        title, head, base = (
            "Test PR to Merge",
            "feature-branch",
            "main",
        )
        logger.info(f"Testing merge_pull_request for {owner}/{repo}")
        pr = create_pull_request(
            owner, repo, title, head, base, body="Test PR Body"
        )
        pr_number = pr["number"]
        result = merge_pull_request(owner, repo, pr_number)
        assert result[
            "merged"
        ], "Pull request not merged successfully"
        logger.success("merge_pull_request test passed!")
    except Exception as e:
        logger.error(f"merge_pull_request test failed: {e}")


def test_list_repo_collaborators():
    try:
        from swarms_tools.devs.github import list_repo_collaborators

        owner, repo = "octocat", "Hello-World"
        logger.info(
            f"Testing list_repo_collaborators for {owner}/{repo}"
        )
        result = list_repo_collaborators(owner, repo)
        assert isinstance(result, list), "Result is not a list"
        logger.success("list_repo_collaborators test passed!")
    except Exception as e:
        logger.error(f"list_repo_collaborators test failed: {e}")


def test_add_repo_collaborator():
    try:
        from swarms_tools.devs.github import add_repo_collaborator

        owner, repo = "octocat", "Hello-World"
        username = "test-collaborator"
        logger.info(
            f"Testing add_repo_collaborator for {owner}/{repo} and username: {username}"
        )
        result = add_repo_collaborator(owner, repo, username)
        assert result["permissions"].get(
            "push", False
        ), "Collaborator not added successfully"
        logger.success("add_repo_collaborator test passed!")
    except Exception as e:
        logger.error(f"add_repo_collaborator test failed: {e}")


if __name__ == "__main__":
    logger.info("Starting GitHub function tests...")

    test_get_user_info()
    test_list_repo_issues()
    test_create_issue()
    test_list_open_prs()
    test_get_repo_details()
    test_close_issue()
    test_create_pull_request()
    test_merge_pull_request()
    test_list_repo_collaborators()
    test_add_repo_collaborator()

    logger.info("All tests completed!")
