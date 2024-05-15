import * as cdk from 'aws-cdk-lib';
import { Match, Template } from 'aws-cdk-lib/assertions';
import {DomainStack} from '../lib/domain-stack';

test("Hosted zone created", () => {
    const crossAccountId = 'test-cross-account-id'
    const app = new cdk.App();
    const stack = new DomainStack(app, 'DomainStack-test', {
        crossAccountId: crossAccountId
    });

    const template = Template.fromStack(stack);

    template.hasResourceProperties('AWS::Route53::HostedZone', {
        Name: "suojattudata.suomi.fi."
    })

    template.hasResourceProperties('AWS::IAM::Role', {
        RoleName: 'Route53CrossDelegateRole',
        AssumeRolePolicyDocument: {
            Statement: Match.arrayWith([Match.objectLike({
                    Action: "sts:AssumeRole",
                    Principal: {
                        AWS: {
                            'Fn::Join': Match.arrayWith([
                                Match.arrayWith([
                                    Match.stringLikeRegexp(`.*${crossAccountId}.*`)
                                ])
                            ])
                        }
                    }
            })])
        }
    })
})
