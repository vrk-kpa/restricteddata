import {aws_rds, aws_kms, StackProps} from "aws-cdk-lib";
import {CommonStackProps} from "./common-stack-props";

export interface LambdaStackProps extends CommonStackProps {
  ckanInstance: aws_rds.IDatabaseInstance;
  ckanAdminCredentials: aws_rds.Credentials;
  secretsEncryptionKey: aws_kms.IKey;
}
