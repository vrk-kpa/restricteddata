import { Stack } from 'aws-cdk-lib';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as efs from 'aws-cdk-lib/aws-efs';

import { Construct } from 'constructs';

import { EfsStackProps } from './efs-stack-props';

export class FileSystemStack extends Stack {
  readonly solrFs: efs.FileSystem;

  constructor(scope: Construct, id: string, props: EfsStackProps) {
    super(scope, id, props);

    this.solrFs = new efs.FileSystem(this, 'solrFs', {
      vpc: props.vpc,
      performanceMode: efs.PerformanceMode.GENERAL_PURPOSE,
      throughputMode: efs.ThroughputMode.BURSTING,
      vpcSubnets: {
        subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS,
      },
      encrypted: true,
    });

  }
}
