#!/usr/bin/env node
import * as cdk from '@aws-cdk/core';
import { AwsCdkDemoStack } from '../lib/aws-cdk-demo-stack';

const app = new cdk.App();
new AwsCdkDemoStack(app, 'AwsCdkDemoStack');
