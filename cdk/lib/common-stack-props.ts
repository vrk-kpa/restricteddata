import {StackProps} from "aws-cdk-lib";
import {IVpc} from "aws-cdk-lib/aws-ec2";
import {EnvProps} from "./env-props";

export interface CommonStackProps extends StackProps {
  envProps: EnvProps;
  environment: string;
  vpc: IVpc;
}
