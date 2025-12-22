# CI/CD Guide with GitHub Actions

This guide explains how to set up and maintain the Continuous Integration/Continuous Deployment (CI/CD) pipeline for the Link Shortener.

## What is CI/CD?
- **CI (Continuous Integration)**: Automatically testing code when you make changes.
- **CD (Continuous Deployment)**: Automatically deploying your code to production (AWS) when changes are approved.

## Workflow Overview
We use **GitHub Actions** to automate deployment. The workflow is defined in `.github/workflows/deploy.yml`.

### Triggers
The pipeline runs automatically when:
- You push code to the `main` branch.
- You manually trigger it from the "Actions" tab in GitHub.

## Setup Instructions

### 1. GitHub Secrets
For the pipeline to access your AWS account, you must set up secrets in your GitHub Repository settings:

1.  Go to **Settings** > **Secrets and variables** > **Actions**.
2.  Click **New repository secret**.
3.  Add the following secrets:
    *   `AWS_ACCESS_KEY_ID`: Your IAM User Access Key.
    *   `AWS_SECRET_ACCESS_KEY`: Your IAM User Secret Key.
    *   `AWS_REGION`: e.g., `us-east-1`.
    *   `S3_BUCKET_NAME`: The name of your S3 bucket hosting the frontend.
    *   `LAMBDA_CREATE_FUNCTION_NAME`: Name of the Create Link Lambda (e.g., `SimpleLink-Create`).
    *   `LAMBDA_REDIRECT_FUNCTION_NAME`: Name of the Redirect Lambda (e.g., `SimpleLink-Redirect`).

### 2. The Workflow File
The file is located at `.github/workflows/deploy.yml`. It performs two main jobs:

#### Job 1: Deploy Backend (Lambda)
- Zips the Python code in `src/backend/create_link`.
- Updates the AWS Lambda function code using AWS CLI.
- Repeat for `redirect`.

#### Job 2: Deploy Frontend (S3)
- Syncs the `src/frontend` folder to your S3 bucket.
- Sets public read permissions (if required by your bucket policy).

## Monitoring
Check the "Actions" tab in your GitHub repository to see the status of deployments. Green means success!
