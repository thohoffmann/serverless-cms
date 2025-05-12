# Serverless Content Management System (CMS) on AWS

## Overview

This project is a scalable, cost-effective Content Management System (CMS) built using AWS serverless technologies. The CMS exposes a RESTful API for managing and retrieving content, making it suitable for websites, apps, and other digital platforms.

---

## Architecture Diagrams

### High Level Architecture
![High Level Architecture](architecture_high_level.png)

### Service Level Architecture
![Service Level Architecture](architecture_service_level.png)

### Detailed Implementation
![Detailed Implementation](architecture_detailed.png)

---

## Features

- **API-driven**: All content operations (CRUD) are performed via a secure API.
- **Serverless**: Utilizes AWS Lambda, API Gateway, DynamoDB, and S3 for a fully managed, pay-as-you-go architecture.
- **Scalable**: Automatically scales with demand.
- **Secure**: Supports authentication and authorization (e.g., via AWS Cognito).
- **Extensible**: Easily add new content types or endpoints.

---

## Architecture

- **API Gateway**: Exposes RESTful endpoints for content operations.
- **AWS Lambda**: Handles business logic for each API endpoint.
- **DynamoDB**: Stores structured content (e.g., articles, metadata).
- **S3**: Stores unstructured content (e.g., images, files).
- **Cognito**: (Optional) Manages user authentication and authorization.
- **CloudFormation/SAM/CDK**: Infrastructure as Code for repeatable deployments.

---

## API Documentation

The API documentation is available through Swagger UI. To view it:

1. Start the local server:
   ```bash
   http-server -o
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:8080/swagger-ui.html
   ```

### API Overview

The CMS API provides a RESTful interface for managing content. All endpoints are prefixed with `/content` and support standard CRUD operations.

#### Base URL
```
https://fumzzf8i07.execute-api.eu-west-2.amazonaws.com/prod
```

#### Authentication
Currently, the API is open for testing. Future versions will implement AWS Cognito for authentication.

#### Content Types
The API supports the following content types:
- Articles
- Pages
- Media files (stored in S3)

#### Endpoints

##### List All Content
```
GET /content
```
Returns a list of all content items with pagination support.

##### Get Content by ID
```
GET /content/{id}
```
Retrieves a specific content item by its ID.

##### Create Content
```
POST /content
```
Creates a new content item. Required fields:
- `title`: string
- `content`: string
- `author`: string
- `timestamp`: ISO date string (optional)

##### Update Content
```
PUT /content/{id}
```
Updates an existing content item. All fields are optional.

##### Delete Content
```
DELETE /content/{id}
```
Removes a content item from the system.

#### Response Format
All responses follow this structure:
```json
{
  "message": "Success message",
  "path": "/content/{id}",
  "method": "GET|POST|PUT|DELETE",
  "time": "2024-04-28T12:00:00Z"
}
```

#### Error Handling
The API uses standard HTTP status codes:
- 200: Success
- 400: Bad Request
- 404: Not Found
- 500: Server Error

Error responses include:
```json
{
  "error": "Error message",
  "code": "ERROR_CODE",
  "details": "Additional error details"
}
```

### Interactive Documentation
The Swagger UI provides:
- All available API endpoints
- Request/response schemas
- Interactive API testing interface
- Detailed documentation for each endpoint
- Example requests and responses

---

## Project Plan

### 1. Requirements & Design

- Define content types and data models (e.g., articles, pages, media).
- Design API endpoints (e.g., `GET /content/{id}`, `POST /content`).
- Plan authentication/authorization strategy.

### 2. Infrastructure Setup

- Set up AWS account and IAM roles.
- Define infrastructure using AWS SAM, CDK, or CloudFormation.

### 3. API Development

- Create API Gateway REST API.
- Implement Lambda functions for:
  - Creating content
  - Retrieving content
  - Updating content
  - Deleting content
- Integrate Lambda with DynamoDB and S3.

### 4. Data Storage

- Design DynamoDB tables for content metadata.
- Set up S3 buckets for media storage.

### 5. Security

- Implement authentication (e.g., Cognito).
- Set up IAM roles and policies for least-privilege access.
- Enable API Gateway authorization.

### 6. Testing

- Write unit and integration tests for Lambda functions.
- Test API endpoints using tools like Postman.

### 7. Deployment

- Automate deployment with CI/CD (e.g., GitHub Actions, CodePipeline).
- Document deployment steps.

### 8. Documentation

- Document API endpoints (OpenAPI/Swagger).
- Provide usage examples.

### 9. Monitoring & Logging

- Enable CloudWatch logging for Lambda and API Gateway.
- Set up alarms for errors and performance issues.

---

## Example API Endpoints

- `GET /content/{id}` – Retrieve content by ID
- `POST /content` – Create new content
- `PUT /content/{id}` – Update content
- `DELETE /content/{id}` – Delete content
- `GET /content` – List content (with filters)

---

## Getting Started

1. Clone the repository.
2. Install dependencies.
3. Deploy the stack using your chosen IaC tool.
4. Use the provided API endpoints to manage content.

---

## Next Steps

Now that the serverless CMS infrastructure is in place with full CRUD functionality, here are the next development priorities:

### 1. ✅ Lambda Implementation (Completed)
- Add support for content versioning

### 2. Authentication & Authorization
- Implement AWS Cognito for user management
  - Set up user pools and identity pools
  - Configure user groups and roles
- Add JWT authentication to API Gateway
- Implement fine-grained access control for different content types

### 3. Media Management
- Enhance S3 integration for media files
  - Implement secure upload/download flows
  - Add media optimization (resizing, compression)
  - Support for metadata and tagging
- Create dedicated media endpoints

### 4. Admin Interface
- Develop a web-based admin dashboard
  - Content creation and management UI
  - User and permission management
  - Media library
- Host on S3 with CloudFront distribution

### 5. CI/CD Pipeline
- Set up GitHub Actions or AWS CodePipeline
  - Automated testing
  - Automated deployment to staging/production
  - Infrastructure validation

### 6. Enhanced Monitoring
- Add detailed CloudWatch metrics and dashboards
- Set up alerting for performance issues and errors
- Implement distributed tracing with AWS X-Ray

## Progress Update

### Completed Steps:
1. ✅ Requirements & Design
2. ✅ Infrastructure Setup - Deployed using AWS CDK
3. ✅ API Development
   - Created Lambda function with CRUD operations
   - Integrated with DynamoDB for data persistence
   - Implemented error handling and validation
   - Setup proper API responses
4. ✅ Data Storage - DynamoDB table for content
5. ✅ Testing - Created API test page and validated functionality

### Next Steps:
1. Authentication & Authorization
2. Media Management
3. Admin Interface
4. CI/CD Pipeline
5. Enhanced Monitoring

## Testing the API

You can test the API in several ways:

### 1. Using the API Test Page

Open the `api-test.html` file in your browser to interactively test all API endpoints. This page allows you to:
- Create new content
- Retrieve content by ID
- List all content
- Update existing content
- Delete content

### 2. Using cURL

```bash
# List all content
curl https://fumzzf8i07.execute-api.eu-west-2.amazonaws.com/prod/content

# Create content
curl -X POST https://fumzzf8i07.execute-api.eu-west-2.amazonaws.com/prod/content \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Title","content":"Test Content","author":"Test Author"}'

# Get content by ID
curl https://fumzzf8i07.execute-api.eu-west-2.amazonaws.com/prod/content/{id}

# Update content
curl -X PUT https://fumzzf8i07.execute-api.eu-west-2.amazonaws.com/prod/content/{id} \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated Title","content":"Updated Content"}'

# Delete content
curl -X DELETE https://fumzzf8i07.execute-api.eu-west-2.amazonaws.com/prod/content/{id}
```

### 3. Using Swagger UI

You can also use the Swagger UI documentation:
1. Start the local server: `http-server -o`
2. Open your browser and navigate to: `http://localhost:8000/cdk-app/swagger-ui.html`

---

## Contributing

Contributions are welcome! Please open issues or submit pull requests.

---

## License

MIT License

## API Test Page

A simple HTML page has been created to test the API endpoints for the serverless CMS. This page allows you to:

1. Create new content
2. Retrieve content by ID
3. List all content items
4. Update existing content
5. Delete content items

To use the API test page:

1. Open the `api-test.html` file in your browser
2. The page will automatically fetch and display all existing content
3. Use the forms to interact with the API endpoints

All API calls are made directly to the deployed AWS API Gateway endpoint defined in the Swagger specification. 