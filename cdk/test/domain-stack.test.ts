import * as cdk from 'aws-cdk-lib';
import { Template } from 'aws-cdk-lib/assertions';
import {DomainStack} from '../lib/domain-stack';

test("Hosted zone created", () => {
    const app = new cdk.App();
    const stack = new DomainStack(app, 'DomainStack-test', {
    });

    const template = Template.fromStack(stack);

    template.hasResourceProperties('AWS::Route53::HostedZone', {
        Name: "suojattudata.suomi.fi."
    })
})
