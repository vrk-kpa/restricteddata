import {aws_iam, aws_route53, aws_route53_targets, Stack} from "aws-cdk-lib";
import {Construct} from "constructs";
import {SubDomainStackProps} from "./sub-domain-stack-props";

export class SubDomainStack extends Stack {
    constructor(scope: Construct, id: string, props: SubDomainStackProps) {
        super(scope, id, props);


        const subZone = new aws_route53.PublicHostedZone(this, 'SubZone', {
            zoneName: props.recordName + ".rekisteridata.fi"
        })

        if (props.prodAccountId) {
            const delegationRoleArn = Stack.of(this).formatArn({
                region: props.env?.region,
                service: 'iam',
                account: props.prodAccountId,
                resource: 'role',
                resourceName: 'Route53CrossDelegateRole'
            })

            const delegationRole = aws_iam.Role.fromRoleArn(this, 'delegationRole', delegationRoleArn)

            new aws_route53.CrossAccountZoneDelegationRecord(this, 'delegate', {
                delegatedZone: subZone,
                delegationRole: delegationRole,
                parentHostedZoneName: "rekisteridata.fi"
            })
        }


        let record = new aws_route53.ARecord(this, 'subDomainRecord', {
            zone: subZone,
            recordName: props.recordName,
            target: aws_route53.RecordTarget.fromAlias(new aws_route53_targets.LoadBalancerTarget(props.loadBalancer))
        })




    }

}