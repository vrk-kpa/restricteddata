import {aws_ec2, aws_rds, StackProps} from "aws-cdk-lib";
import {CommonStackProps} from "./common-stack-props";

export interface LambdaStackProps extends CommonStackProps {
  ckanInstance: aws_rds.IDatabaseInstance;
  ckanAdminCredentials: aws_rds.Credentials;
  vpc: aws_ec2.IVpc;
}
