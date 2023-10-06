import {aws_ec2, aws_s3, Duration, Stack} from "aws-cdk-lib";
import {Construct} from "constructs";
import {ApplicationLoadBalancer} from "aws-cdk-lib/aws-elasticloadbalancingv2";
import {CommonStackProps} from "./common-stack-props";
import {BucketEncryption} from "aws-cdk-lib/aws-s3";

export class LoadBalancerStack extends Stack {
  readonly loadBalancer: ApplicationLoadBalancer
  constructor(scope: Construct, id: string, props: CommonStackProps) {
    super(scope, id, props);

    const secGroup = new aws_ec2.SecurityGroup(this, 'loadBalancerSecurityGroup', {
      vpc: props.vpc,
    })

    secGroup.addIngressRule(aws_ec2.Peer.anyIpv4(), aws_ec2.Port.tcp(443), "HTTPS from anywhere")

    this.loadBalancer = new ApplicationLoadBalancer(this, 'LoadBalancer', {
      vpc: props.vpc,
      internetFacing: true,
      vpcSubnets: {
        subnets: props.vpc.publicSubnets
      },
      securityGroup: secGroup
    })

    const logBucket = new aws_s3.Bucket(this, 'logBucket', {
      bucketName: `registrydata-${props.environment}-loadbalancer-logs`,
      blockPublicAccess: aws_s3.BlockPublicAccess.BLOCK_ALL,
      encryption: BucketEncryption.S3_MANAGED,
      versioned: true,
      lifecycleRules: [
        {
          enabled: true,
          expiration: Duration.days(30)
        }
      ]
    })
  }
}
