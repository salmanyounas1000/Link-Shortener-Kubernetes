# Deep Dive: IP Restriction and CI/CD Setup

This document explains the technical details of the IP restriction implementation and provides a step-by-step guide for setting up the CI/CD pipeline.

---

## Part 1: IP Restriction Implementation

### How it Works
The IP restriction mechanism does **not** rely on external firewalls like AWS WAF (which costs extra). Instead, it is implemented purely in **application logic** within the Lambda function and **DynamoDB**.

1.  **Extracting the IP**:
    When a user calls your API, AWS API Gateway captures their IP address and passes it to Lambda in the `event` object.
    *   **REST API**: `event['requestContext']['identity']['sourceIp']`
    *   **HTTP API**: `event['requestContext']['http']['sourceIp']`
    *(The code has been updated to handle both automatically)*

2.  **Tracking Usage in DynamoDB**:
    We create a special counter item in your database for every IP address, every month.
    *   **Key Format**: `RATELIMIT#<User_IP>#2024-05`
    *   **Logic**: Every time someone tries to create a link, we increment this counter.

3.  **Enforcing the Limit**:
    We use a **Conditional Update** in DynamoDB. This is a powerful feature that says:
    > "Increment this counter ONLY IF it is currently less than 10. If it's 10 or more, fail the request."
    
    If DynamoDB says "ConditionalCheckFailed", we know the user hit their limit, and we return a `429 Too Many Requests` error.

### What You Need to configure in AWS
Since this logic is in the code, you don't need to configure complex network rules. However, you must ensure your **Lambda Execution Role** has permission to update items in DynamoDB.

**Required IAM Permissions**:
Your Lambda role likely already has these, but verify it has:
*   `dynamodb:GetItem`
*   `dynamodb:PutItem`
*   `dynamodb:UpdateItem` (Critical for the counter)

---

## Part 2: CI/CD Pipeline (YAML File) Explained

The file `.github/workflows/deploy.yml` instructs GitHub on how to deploy your code. Here is the translation:

### The "Trigger"
```yaml
on:
  push:
    branches:
      - main
```
**Translation:** "Run this automation whenever someone pushes code to the `main` branch."

### Job 1: Backend Deployment
1.  **Checkout**: Downloads your code to the build server.
2.  **Configure AWS**: Logs in to AWS using the secrets you provided.
3.  **Zip**: Compresses the python files (`lambda_function.py`) into a `.zip` file.
    *   *Why?* Lambda requires code to be uploaded as a zip.
4.  **Deploy**: Runs the AWS CLI command:
    `aws lambda update-function-code ...`
    This uploads the new zip file to your existing Lambda function.

### Job 2: Frontend Deployment
1.  **Sync**: Runs the AWS CLI command:
    `aws s3 sync ./src/frontend s3://YOUR_BUCKET ...`
    This copies your HTML/JS/CSS files to your S3 bucket, effectively updating your website.

---

## Part 3: Step-by-Step Setup Guide

To make the CI/CD pipeline work, you need to "connect" GitHub to your AWS account.

### Step 1: Create an IAM User for GitHub
1.  Login to AWS Console and go to **IAM**.
2.  Click **Users** -> **Create user**.
3.  Name it `github-actions-deployer`.
4.  **Permissions**: Attach the following policies (or create a custom one):
    *   `AWSLambda_FullAccess` (or specific permission to update your functions)
    *   `AmazonS3FullAccess` (to upload to your bucket)
5.  **Create Access Keys**:
    *   Click on the new user -> **Security credentials** tab.
    *   "Create access key" -> Select "Command Line Interface (CLI)".
    *   **COPY THESE KEY VALUES!** Access Key ID and Secret Access Key. You won't see them again.

### Step 2: Add Secrets to GitHub
1.  Go to your GitHub Repository.
2.  Click **Settings** (top right tab).
3.  On the left sidebar, find **Secrets and variables** -> **Actions**.
4.  Click the green **New repository secret** button.
5.  Add the following 6 secrets:

| Secret Name | Value Example |
| :--- | :--- |
| `AWS_ACCESS_KEY_ID` | `AKIAIOSFODNN7EXAMPLE` (From Step 1) |
| `AWS_SECRET_ACCESS_KEY` | `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY` (From Step 1) |
| `AWS_REGION` | `us-east-1` (Where your AWS resources are) |
| `S3_BUCKET_NAME` | `my-link-shortener-website` (Just the name, no http://) |
| `LAMBDA_CREATE_FUNCTION_NAME` | `simple-link-create` (The exact name of your Lambda function in AWS) |
| `LAMBDA_REDIRECT_FUNCTION_NAME` | `simple-link-redirect` |

### Step 3: Trigger a Deploy
1.  Make a small change to your code (e.g., update the README).
2.  Commit and push to `main`.
3.  Go to the **Actions** tab in GitHub.
4.  You should see a workflow running. Click it to watch the live logs!
