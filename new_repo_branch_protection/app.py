import json
import os
from github import Github
from github import GithubException

g = Github(os.environ["GITHUB_TOKEN"])
org = os.environ["GITHUB_ORG"]
default_branch = os.environ["GITHUB_DEFAULT_BRANCH"]
admin = os.environ["GITHUB_ADMIN_NAME"]

def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    body = json.loads(event["body"])
    response = {}
    if "action" in body and "created" in body["action"]:
        try: 
            repo_name = body["repository"]["name"]
            repo = g.get_repo(f"{org}/{repo_name}")
            if len(list(repo.get_branches())) == 0:
                print("The repo is empty without a branch. Creating a master branch with standard README.md")
                resp = repo.create_file("README.md", "init commit", "This file is created automatically by GitHub branch protection lambda", branch=default_branch)

            # This will add all the protection rule options and not remove any existing options if there is a rule existed. 
            print("Adding branch protection rule ...")
            repo.get_branch(default_branch).edit_protection(required_approving_review_count=2, enforce_admins=True)

            # verify master branch protection
            if repo.get_branch(default_branch).protected:
                issue = repo.create_issue(title="Master branch is now protected", body=f"Master branch is now protected by branch protection rule. Please contact @{admin} for more detail")
                issue.edit(state='closed')
                response = {
                    "statusCode": 200,
                    "body": json.dumps({
                        "message": "Master branch is now protected by branch protection rule",
                    }),
                }
            else:
                raise Exception("Something is not running as expected. Master branch is not protected.")

        except Exception as e:
            print(e)
            response = {
                "statusCode": 500,
                "body": json.dumps({
                    "message": "Error occurs while adding branch protection rule",
                }),
            }
    
    print(response)
    return response

