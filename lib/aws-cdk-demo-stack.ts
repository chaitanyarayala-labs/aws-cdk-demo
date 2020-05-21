import * as cdk from '@aws-cdk/core';
import * as lambda from '@aws-cdk/aws-lambda';
import * as api from '@aws-cdk/aws-apigateway';

export class AwsCdkDemoStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
    super(scope, id, props);
    
    // defines an AWS Lambda resource
    const hello = new lambda.Function(this, 'HelloHandler', {
        runtime: lambda.Runtime.NODEJS_10_X, //execution environment
        code: lambda.Code.fromAsset('lambda'), //code loaded from "lambda" directory
        handler: 'hello.handler' //file is "hello", function is "handler"
    });

    // define an AWS APIGateway REST API resource backed by our "hello" function.
    new api.LambdaRestApi(this, 'Endpoint', {
      handler: hello
    });
  }
}
