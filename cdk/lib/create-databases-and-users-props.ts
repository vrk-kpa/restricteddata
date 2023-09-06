import {aws_kms, aws_rds, StackProps} from "aws-cdk-lib";
import {CommonStackProps} from "./common-stack-props";

export interface CreateDatabasesAndUsersProps extends CommonStackProps{
  ckanInstance: aws_rds.IDatabaseInstance,
  ckanAdminCredentials: aws_rds.Credentials,
  secretsEncryptionKey: aws_kms.IKey;
}
