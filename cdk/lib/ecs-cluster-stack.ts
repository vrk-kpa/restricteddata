import {aws_ecs, Stack} from "aws-cdk-lib";
import {Construct} from "constructs";
import {CommonStackProps} from "./common-stack-props";

export class EcsClusterStack extends Stack {
  readonly cluster: aws_ecs.ICluster;
  constructor(scope: Construct, id: string, props: CommonStackProps) {
    super(scope, id, props);

    this.cluster = new aws_ecs.Cluster(this, 'ECSCluster', {
      vpc: props.vpc,
      enableFargateCapacityProviders: true
    })

  }
}
