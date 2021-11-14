# github-new-repo-branch-protection

A simple web service that listens for GitHub organization events to know when a repository has been created and automatically creates the protection of the main branch

This project contains source code and supporting files for a serverless application that you can deploy with the SAM CLI. It includes the following files and folders.

- new_repo_branch_protection - Code for the application's Lambda function and Project Dockerfile.
- events - Invocation events that you can use to invoke the function.
- tests - Unit tests for the application code. 
- template.yaml - A template that defines the application's AWS resources.

The application uses several AWS resources, including Lambda functions and an API Gateway API. These resources are defined in the `template.yaml` file in this project. You can update the template to add AWS resources through the same deployment process that updates your application code.


## Deploy the sample application

The Serverless Application Model Command Line Interface (SAM CLI) is an extension of the AWS CLI that adds functionality for building and testing Lambda applications. It uses Docker to run your functions in an Amazon Linux environment that matches Lambda. It can also emulate your application's build environment and API.

To use the SAM CLI, you need the following tools.

* AWS credential - [AWS Access with permission to create SAM application](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-getting-started-set-up-credentials.html)
* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)
* GitHub Access Token 
  - [Permission to add branch protection rule](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/defining-the-mergeability-of-pull-requests/managing-a-branch-protection-rule)
  - [Create GitHub Access Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)

You may need the following for local testing.
* [Python 3 installed](https://www.python.org/downloads/)

## Build and Deploy
To build and deploy your application for the first time,

1. please provide the following environment variables in `template.yaml`:

```yaml
      Environment:
        Variables:
          GITHUB_TOKEN: <your github token>
          GITHUB_ORG: <your github org>
          GITHUB_DEFAULT_BRANCH: <your github default branch>
          GITHUB_ADMIN_NAME: <your github admin name>
```

2. then run the following in your shell:

```bash
sam build
sam deploy --guided
```

The `sam build` command will build a docker image from a Dockerfile and then copy the source of your application inside the Docker image. The `sam deploy` command will package and deploy your application to AWS, with a series of prompts:

* **Stack Name**: The name of the stack to deploy to CloudFormation. This should be unique to your account and region, and a good starting point would be something matching your project name.
* **AWS Region**: The AWS region you want to deploy your app to.
* **Confirm changes before deploy**: If set to yes, any change sets will be shown to you before execution for manual review. If set to no, the AWS SAM CLI will automatically deploy application changes.
* **Allow SAM CLI IAM role creation**: Many AWS SAM templates, including this example, create AWS IAM roles required for the AWS Lambda function(s) included to access AWS services. By default, these are scoped down to minimum required permissions. To deploy an AWS CloudFormation stack which creates or modifies IAM roles, the `CAPABILITY_IAM` value for `capabilities` must be provided. If permission isn't provided through this prompt, to deploy this example you must explicitly pass `--capabilities CAPABILITY_IAM` to the `sam deploy` command.
* **Save arguments to samconfig.toml**: If set to yes, your choices will be saved to a configuration file inside the project, so that in the future you can just re-run `sam deploy` without parameters to deploy changes to your application.

You can find your API Gateway Endpoint URL in the output values displayed after deployment.

3. Create webhook to send event to the API created in step2 (https://docs.github.com/webhooks/):
    - Payload URL: Copy the value of `NewRepoBranchProtectionApi` from the output in step2 (example url: https://<example_id>.execute-api.us-east-1.amazonaws.com/Prod/rule/   )
    - Content type: application/json
    - Which events would you like to trigger this webhook? -> 
        select `Let me select individual events.`
        select `Pushes`
        select `Repositories`
    - select Active


## Use the SAM CLI to build and test locally

Provide your parameters in `env.json`

```bash
github-new-repo-branch-protection$ vi env.json
```

Build your application with the `sam build` command.

```bash
github-new-repo-branch-protection$ sam build
```

The SAM CLI builds a docker image from a Dockerfile and then installs dependencies defined in `new_repo_branch_protection/requirements.txt` inside the docker image. The processed template file is saved in the `.aws-sam/build` folder.

Test a single function by invoking it directly with a test event. An event is a JSON document that represents the input that the function receives from the event source. Test events are included in the `events` folder in this project.

Run functions locally and invoke them with the `sam local invoke` command.

```bash
github-new-repo-branch-protection$ sam local invoke NewRepoBranchProtectionLambda --event events/event.json --env-vars env.json
```

The SAM CLI reads the application template to determine the API's routes and the functions that they invoke. The `Events` property on each function's definition includes the route and method for each path.

```yaml
      Events:
        NewRepoBranchProtection:
          Type: Api
          Properties:
            Path: /rule
            Method: get
```

## Add a resource to your application
The application template uses AWS Serverless Application Model (AWS SAM) to define application resources. AWS SAM is an extension of AWS CloudFormation with a simpler syntax for configuring common serverless application resources such as functions, triggers, and APIs. For resources not included in [the SAM specification](https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md), you can use standard [AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html) resource types.

## Fetch, tail, and filter Lambda function logs

To simplify troubleshooting, SAM CLI has a command called `sam logs`. `sam logs` lets you fetch logs generated by your deployed Lambda function from the command line. In addition to printing the logs on the terminal, this command has several nifty features to help you quickly find the bug.

`NOTE`: This command works for all AWS Lambda functions; not just the ones you deploy using SAM.

```bash
github-new-repo-branch-protection$ sam logs -n AddBranchProtection --stack-name github-new-repo-branch-protection --tail
```

You can find more information and examples about filtering Lambda function logs in the [SAM CLI Documentation](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-logging.html).

## Unit tests

Tests are defined in the `tests` folder in this project. Use PIP to install the [pytest](https://docs.pytest.org/en/latest/) and run unit tests from your local machine.

```bash
github-new-repo-branch-protection$ pip install pytest pytest-mock --user
github-new-repo-branch-protection$ python -m pytest tests/ -v
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name github-new-repo-branch-protection
```

## Resources

See the [AWS SAM developer guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html) for an introduction to SAM specification, the SAM CLI, and serverless application concepts.