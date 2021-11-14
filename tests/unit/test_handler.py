import json

import pytest

from new_repo_branch_protection import app


@pytest.fixture()
def apigw_event():
    """ Generates API GW Event"""

    return {
        "body": "{\"action\":\"created\",\"repository\":{\"name\":\"repo\"}}",
        }


def test_lambda_handler(apigw_event, mocker):
    #TODO: add test coverage

    # ret = app.lambda_handler(apigw_event, "")
    # data = json.loads(ret["body"])

    # assert ret["statusCode"] == 200
    # assert "message" in ret["body"]
    # assert data["message"] == "Master branch is now protected by branch protection rule"
