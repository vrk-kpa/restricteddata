import {EnvStackProps} from "./env-stack-props";
import {aws_ec2} from "aws-cdk-lib";

export interface NetworkStackProps extends EnvStackProps {
  vpc: aws_ec2.IVpc;
}
