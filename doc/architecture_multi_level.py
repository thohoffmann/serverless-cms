#!/usr/bin/env python3
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import Lambda, LambdaFunction
from diagrams.aws.database import Dynamodb, DynamodbTable
from diagrams.aws.storage import S3
from diagrams.aws.network import APIGateway, CloudFront, Route53
from diagrams.aws.security import Cognito, IAM, WAF
from diagrams.aws.general import Users
from diagrams.aws.mobile import APIGatewayEndpoint
from diagrams.aws.integration import Eventbridge
from diagrams.aws.management import CloudformationTemplate, Cloudwatch
from diagrams.aws.devtools import Codebuild, Codepipeline
from diagrams.onprem.client import Client, User
from diagrams.programming.framework import React

# 1. High-Level Architecture (Cloud View)
with Diagram("Serverless CMS - High Level Architecture", show=True, filename="architecture_high_level", outformat=["png", "pdf"]):
    with Cluster("AWS Cloud"):
        with Cluster("Frontend"):
            frontend = React("Web Client")
        
        with Cluster("API & Compute"):
            api_compute = APIGateway("Content API")
        
        with Cluster("Storage"):
            storage = Dynamodb("Data Storage")
            
        with Cluster("Security"):
            security = Cognito("Authentication")
    
    clients = Client("Users")
    
    clients >> frontend >> api_compute >> storage
    clients >> security >> api_compute

# 2. Mid-Level Architecture (Services View)
with Diagram("Serverless CMS - Service Level", show=True, filename="architecture_service_level", outformat=["png", "pdf"]):
    with Cluster("AWS Cloud"):
        # Frontend Services
        with Cluster("Frontend Services"):
            cloudfront = CloudFront("CloudFront CDN")
            website = S3("Website Hosting")
            dns = Route53("DNS")
        
        # API & Lambda Services
        with Cluster("API & Compute"):
            apigw = APIGateway("API Gateway")
            functions = Lambda("Lambda Functions")
            events = Eventbridge("Events")
        
        # Storage Services
        with Cluster("Storage"):
            dynamo = Dynamodb("DynamoDB")
            s3_content = S3("Media Storage")
        
        # Security Services
        with Cluster("Security"):
            cognito = Cognito("User Authentication")
            waf = WAF("WAF")
            iam = IAM("Permissions")
        
        # DevOps
        with Cluster("DevOps"):
            cicd = Codepipeline("CI/CD Pipeline")
            monitoring = Cloudwatch("Monitoring")
            template = CloudformationTemplate("CloudFormation")
    
    users = Users("End Users")
    
    # Connections
    users >> dns >> cloudfront >> website
    users >> waf >> apigw >> functions
    functions >> dynamo
    functions >> s3_content
    users >> cognito >> apigw
    template - cicd
    functions - monitoring

# 3. Detailed Architecture (Implementation Level)
with Diagram("Serverless CMS - Detailed Implementation", show=True, filename="architecture_detailed", outformat=["png", "pdf"]):
    users = User("End Users")
    
    # Frontend Implementation
    with Cluster("Frontend"):
        with Cluster("Static Website (S3)"):
            s3_website = S3("React App")
        
        with Cluster("CDN"):
            cdn = CloudFront("Content Distribution")
        
        dns = Route53("DNS")
    
    # API Layer
    with Cluster("API Layer"):
        api = APIGateway("API Gateway")
        
        # API Endpoints
        with Cluster("API Endpoints"):
            get_content = APIGatewayEndpoint("GET /content")
            post_content = APIGatewayEndpoint("POST /content")
            get_content_id = APIGatewayEndpoint("GET /content/{id}")
            put_content_id = APIGatewayEndpoint("PUT /content/{id}")
            delete_content_id = APIGatewayEndpoint("DELETE /content/{id}")
    
    # Security
    with Cluster("Security"):
        auth = Cognito("Cognito User Pools")
        waf_protection = WAF("API Protection")
        permissions = IAM("IAM Roles & Policies")
    
    # Lambda Functions
    with Cluster("Business Logic"):
        # Current Implementation
        content_lambda = LambdaFunction("Content Lambda")
        
        # Future Implementation
        with Cluster("Future Lambda Functions"):
            create_lambda = LambdaFunction("Create Content")
            read_lambda = LambdaFunction("Read Content")
            update_lambda = LambdaFunction("Update Content") 
            delete_lambda = LambdaFunction("Delete Content")
            media_lambda = LambdaFunction("Media Handler")
    
    # Storage Implementation
    with Cluster("Storage"):
        with Cluster("DynamoDB"):
            content_table = DynamodbTable("Content Table")
            metadata_table = DynamodbTable("Metadata Table")
        
        with Cluster("S3 Storage"):
            media_bucket = S3("Media Bucket")
            backup_bucket = S3("Backup Bucket")
    
    # Monitoring
    with Cluster("Monitoring & Logging"):
        logs = Cloudwatch("CloudWatch Logs")
        metrics = Cloudwatch("CloudWatch Metrics")
        alarms = Cloudwatch("CloudWatch Alarms")
    
    # Workflow Connections
    users >> dns >> cdn >> s3_website
    users >> Edge(label="Request") >> waf_protection >> api
    
    api >> get_content >> read_lambda
    api >> post_content >> create_lambda
    api >> get_content_id >> read_lambda
    api >> put_content_id >> update_lambda
    api >> delete_content_id >> delete_lambda
    
    create_lambda >> content_table
    read_lambda >> content_table
    update_lambda >> content_table
    delete_lambda >> content_table
    
    media_lambda >> media_bucket
    
    users >> auth >> api
    
    # Logging connections
    content_lambda - logs
    [create_lambda, read_lambda, update_lambda, delete_lambda, media_lambda] - logs
    api - logs 