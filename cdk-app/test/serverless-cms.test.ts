import * as cdk from 'aws-cdk-lib';
import { Template } from 'aws-cdk-lib/assertions';
import { ServerlessCmsStack } from '../lib/serverless-cms-stack';

describe('ServerlessCmsStack', () => {
  let template: Template;

  beforeAll(() => {
    const app = new cdk.App();
    // WHEN
    const stack = new ServerlessCmsStack(app, 'TestServerlessCmsStack');
    // THEN
    template = Template.fromStack(stack);
  });

  test('DynamoDB Table Created', () => {
    template.resourceCountIs('AWS::DynamoDB::Table', 1);
    
    template.hasResourceProperties('AWS::DynamoDB::Table', {
      KeySchema: [
        {
          AttributeName: 'id',
          KeyType: 'HASH'
        }
      ],
      BillingMode: 'PAY_PER_REQUEST'
    });
  });

  test('S3 Bucket Created', () => {
    template.resourceCountIs('AWS::S3::Bucket', 1);
    
    template.hasResourceProperties('AWS::S3::Bucket', {
      VersioningConfiguration: {
        Status: 'Enabled'
      }
    });
  });

  test('Lambda Function Created', () => {
    template.resourceCountIs('AWS::Lambda::Function', 2); // 1 for our function, 1 for auto-delete S3 objects
    
    template.hasResourceProperties('AWS::Lambda::Function', {
      Handler: 'index.handler',
      Runtime: 'nodejs18.x',
      Timeout: 10
    });
  });

  test('API Gateway Created', () => {
    template.resourceCountIs('AWS::ApiGateway::RestApi', 1);
    
    template.hasResourceProperties('AWS::ApiGateway::RestApi', {
      Name: 'Serverless CMS API'
    });
  });

  test('API Methods Created', () => {
    // Test that we have HTTP methods defined
    template.resourceCountIs('AWS::ApiGateway::Method', 8); // Actual number of methods in the stack
    
    // Check for GET method on content endpoint
    template.hasResourceProperties('AWS::ApiGateway::Method', {
      HttpMethod: 'GET',
      AuthorizationType: 'NONE'
    });
    
    // Check for POST method on content endpoint
    template.hasResourceProperties('AWS::ApiGateway::Method', {
      HttpMethod: 'POST',
      AuthorizationType: 'NONE'
    });
  });
}); 