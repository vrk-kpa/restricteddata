import {aws_ec2, Stack} from "aws-cdk-lib";
import {Construct} from "constructs";
import {VpcStackProps} from "./vpc-stack-props";

export class VpcStack extends Stack {
  readonly vpc: aws_ec2.IVpc;

  constructor(scope: Construct, id: string, props: VpcStackProps) {
    super(scope, id, props);

    this.vpc = new aws_ec2.Vpc(this, "Vpc", {
      ipAddresses: aws_ec2.IpAddresses.cidr("10.0.0.0/16"),
      maxAzs: props.maxAzs
    })

  }
}
