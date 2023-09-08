import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import {aws_iam, aws_route53} from "aws-cdk-lib";
import {DomainStackProps} from "./domain-stack-props";

export class DomainStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: DomainStackProps) {

    super(scope, id, props);

    const publicZone = new aws_route53.PublicHostedZone(this, "HostedZone", {
      zoneName: "rekisteridata.fi",
    })
    if (props.crossAccountId) {
      const role = new aws_iam.Role(this, 'Route53CrossDelegateRole', {
        assumedBy: new aws_iam.AccountPrincipal(props.crossAccountId),
        roleName: "Route53CrossDelegateRole"
      })

      publicZone.grantDelegation(role)
    }
  }
}
