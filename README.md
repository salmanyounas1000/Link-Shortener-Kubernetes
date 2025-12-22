# Simple Link Shortener

A secure, serverless URL shortener built with AWS Lambda, API Gateway, and DynamoDB. Designed for performance and reliability.

**Created by Salman Younas**  
[hafizsalman1000@gmail.com](mailto:hafizsalman1000@gmail.com)  
[LinkedIn Profile](https://www.linkedin.com/in/salmanyounas1000/)  
[Portfolio](https://salman-devops-portfolio.s3.ap-northeast-1.amazonaws.com/index.html)


## Features

- **Serverless Architecture**: 100% serverless using AWS Lambda.
- **High Performance**: Direct DynamoDB integration for low latency.
- **Secure**:
  - **Creation Limit**: 1 IP can only create 10 links per month.
  - **Usage Limit**: Each link is limited to 20 redirects per month to prevent cost overruns (DDoS protection layer).
- **Clean UI**: Modern, dark-themed interface similar to Vercel/Next.js.

## Tech Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript (hosted on S3).
- **Backend**: Python 3.9 (AWS Lambda).
- **Database**: AWS DynamoDB.
- **API**: AWS API Gateway (REST API).
- **CI/CD**: GitHub Actions.

## Project Structure

```
├── .github/workflows/   # CI/CD Pipelines
├── docs/                # Documentation
├── src/
│   ├── backend/         # Lambda Functions
│   │   ├── create_link/ # Link Creation Logic
│   │   └── redirect/    # Redirection Logic
│   └── frontend/        # Static Website
```

## Security & Limits

To prevent abuse and manage costs (Free Tier eligibility), the following limits are enforced:

1.  **Rate Limiting**: Users are limited to creating **10 links per month** per IP address.
2.  **Access Limiting**: Each generated link allows **20 redirects per month**.
3.  **DDoS Protection**: Basic application-level rate limiting is implemented. For production environments, AWS WAF is recommended.

## Deployment

This project uses **GitHub Actions** for CI/CD.

1.  Push to `main` branch triggers the deployment pipeline.
2.  The pipeline deploys backend code to AWS Lambda and frontend code to S3.

For manual deployment instructions, see `docs/CI_CD_GUIDE.md`.

## License

Private Project. All rights reserved.
