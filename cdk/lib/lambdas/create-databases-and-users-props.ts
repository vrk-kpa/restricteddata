import {aws_kms, aws_rds, StackProps} from "aws-cdk-lib";

import {NetworkStackProps} from "../network-stack-props";

export interface CreateDatabasesAndUsersProps extends NetworkStackProps {
  ckanInstance: aws_rds.IDatabaseInstance,
  ckanAdminCredentials: aws_rds.Credentials,
  secretsEncryptionKey: aws_kms.IKey;
}
