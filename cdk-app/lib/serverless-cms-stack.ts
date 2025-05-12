import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as path from 'path';

export class ServerlessCmsStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // S3 bucket for media
    const mediaBucket = new s3.Bucket(this, 'MediaBucket', {
      versioned: true,
      removalPolicy: cdk.RemovalPolicy.DESTROY, // NOT for production!
      autoDeleteObjects: true, // NOT for production!
    });

    // DynamoDB table for content
    const contentTable = new dynamodb.Table(this, 'ContentTable', {
      partitionKey: { name: 'id', type: dynamodb.AttributeType.STRING },
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
      removalPolicy: cdk.RemovalPolicy.DESTROY, // NOT for production!
    });

    // Create the Lambda function for content API using the code in src/lambda
    const contentFunction = new lambda.Function(this, 'ContentFunction', {
      runtime: lambda.Runtime.NODEJS_18_X,
      handler: 'contentHandler.handler',
      code: lambda.Code.fromAsset(path.join(__dirname, '../src/lambda')),
      timeout: cdk.Duration.seconds(30),
      environment: {
        CONTENT_TABLE_NAME: contentTable.tableName,
        MEDIA_BUCKET_NAME: mediaBucket.bucketName
      }
    });

    // Grant Lambda permissions to access DynamoDB and S3
    contentTable.grantReadWriteData(contentFunction);
    mediaBucket.grantReadWrite(contentFunction);

    // Create API Gateway
    const api = new apigateway.RestApi(this, 'ContentApi', {
      restApiName: 'Serverless CMS API',
      description: 'API for content management',
      defaultCorsPreflightOptions: {
        allowOrigins: apigateway.Cors.ALL_ORIGINS,
        allowMethods: apigateway.Cors.ALL_METHODS,
        allowHeaders: ['Content-Type', 'X-Amz-Date', 'Authorization', 'X-Api-Key', 'X-Amz-Security-Token']
      },
    });

    // Add /content resource
    const contentResource = api.root.addResource('content');
    
    // Integrate Lambda with API Gateway
    const contentIntegration = new apigateway.LambdaIntegration(contentFunction);
    
    // Add GET, POST methods
    contentResource.addMethod('GET', contentIntegration);
    contentResource.addMethod('POST', contentIntegration);
    
    // Add item-specific methods
    const contentItemResource = contentResource.addResource('{id}');
    contentItemResource.addMethod('GET', contentIntegration);
    contentItemResource.addMethod('PUT', contentIntegration);
    contentItemResource.addMethod('DELETE', contentIntegration);

    // Outputs
    new cdk.CfnOutput(this, 'ApiEndpoint', {
      value: api.url,
      description: 'API Gateway endpoint URL',
    });

    new cdk.CfnOutput(this, 'MediaBucketName', {
      value: mediaBucket.bucketName,
      description: 'S3 bucket for media storage',
    });

    new cdk.CfnOutput(this, 'ContentTableName', {
      value: contentTable.tableName,
      description: 'DynamoDB table for content',
    });
  }
} 