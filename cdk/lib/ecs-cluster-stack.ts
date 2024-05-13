import {aws_ecs, aws_servicediscovery, Stack} from "aws-cdk-lib";
import {Construct} from "constructs";
import {NetworkStackProps} from "./network-stack-props";

export class EcsClusterStack extends Stack {
  readonly cluster: aws_ecs.ICluster;
  readonly namespace: aws_servicediscovery.INamespace;
  constructor(scope: Construct, id: string, props: NetworkStackProps) {
    super(scope, id, props);

    this.cluster = new aws_ecs.Cluster(this, 'ECSCluster', {
      vpc: props.vpc,
      enableFargateCapacityProviders: true
    })

    this.namespace = new aws_servicediscovery.PrivateDnsNamespace(this, 'namespace', {
      name: `${props.environment}-opendata-ns`,
      vpc: props.vpc,
    });

  }
}
