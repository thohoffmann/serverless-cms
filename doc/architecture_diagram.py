#!/usr/bin/env python3
from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb, DynamodbTable
from diagrams.aws.storage import S3
from diagrams.aws.network import APIGateway
from diagrams.aws.security import Cognito
from diagrams.aws.general import Users
from diagrams.aws.mobile import APIGatewayEndpoint
from diagrams.aws.network import CloudFront

# Create a diagram
with Diagram("Serverless CMS Architecture", show=True, filename="serverless_cms_architecture"):
    # User and client applications
    users = Users("Clients/Users")
    
    # API Gateway cluster
    with Cluster("API Layer"):
        api = APIGateway("API Gateway")
        endpoints = [
            APIGatewayEndpoint("GET /content"),
            APIGatewayEndpoint("POST /content"),
            APIGatewayEndpoint("GET /content/{id}"),
            APIGatewayEndpoint("PUT /content/{id}"),
            APIGatewayEndpoint("DELETE /content/{id}")
        ]
    
    # Authentication (future)
    with Cluster("Authentication"):
        cognito = Cognito("User Authentication")
    
    # Lambda functions cluster
    with Cluster("Business Logic"):
        content_lambda = Lambda("Content Lambda")
        
        # We'll have these in the future
        future_lambdas = [
            Lambda("Create Content"),
            Lambda("Read Content"),
            Lambda("Update Content"),
            Lambda("Delete Content"),
            Lambda("Media Handler")
        ]
    
    # Storage cluster
    with Cluster("Storage"):
        dynamodb = DynamodbTable("Content Table")
        s3_bucket = S3("Media Bucket")
    
    # Front end (future)
    with Cluster("Frontend (Future)"):
        cloudfront = CloudFront("CloudFront")
        s3_website = S3("Static Website")
    
    # Connect the components
    users >> api
    api >> endpoints
    
    # Current implementation connections
    endpoints >> content_lambda
    content_lambda >> dynamodb
    content_lambda >> s3_bucket
    
    # Authentication (future)
    users >> cognito
    cognito >> api
    
    # Frontend (future)
    users >> cloudfront >> s3_website 