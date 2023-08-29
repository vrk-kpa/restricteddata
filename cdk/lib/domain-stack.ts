import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import {aws_route53} from "aws-cdk-lib";
// import * as sqs from 'aws-cdk-lib/aws-sqs';

export class DomainStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    new aws_route53.PublicHostedZone(this, "HostedZone", {
      zoneName: "rekisteridata.fi"
    })

  }
}
