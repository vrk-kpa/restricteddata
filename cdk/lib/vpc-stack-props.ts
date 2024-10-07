import {StackProps} from "aws-cdk-lib";

export interface VpcStackProps extends StackProps {
  maxAzs: number
}
