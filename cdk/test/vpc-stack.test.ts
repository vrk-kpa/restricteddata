import * as cdk from 'aws-cdk-lib';
import { Template } from 'aws-cdk-lib/assertions';
import { VpcStack } from '../lib/vpc-stack';

test('VPC Created with given cidr block', () => {
    const app = new cdk.App();
    const stack = new VpcStack(app, 'VpcStack-test');

    const template = Template.fromStack(stack);

    template.hasResourceProperties('AWS::EC2::VPC', {
        CidrBlock: "10.0.0.0/16"
   });
});
