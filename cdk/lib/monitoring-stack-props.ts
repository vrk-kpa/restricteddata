import { NodejsFunction } from 'aws-cdk-lib/aws-lambda-nodejs';
import {StackProps} from "aws-cdk-lib";

export interface MonitoringStackProps extends StackProps {
  sendToZulipLambda: NodejsFunction
}

