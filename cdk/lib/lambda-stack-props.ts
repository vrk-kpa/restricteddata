import {aws_rds, aws_kms, StackProps} from "aws-cdk-lib";
import {NetworkStackProps} from "./network-stack-props";

export interface LambdaStackProps extends NetworkStackProps {
  ckanInstance: aws_rds.IDatabaseInstance;
  ckanAdminCredentials: aws_rds.Credentials;
}
