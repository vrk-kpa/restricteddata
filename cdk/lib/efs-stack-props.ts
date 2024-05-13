import * as ec2 from 'aws-cdk-lib/aws-ec2';

import {NetworkStackProps} from "./network-stack-props";

export interface EfsStackProps extends NetworkStackProps {
  terminationProtection: boolean;
}
