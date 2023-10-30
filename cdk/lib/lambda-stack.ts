
import {CreateDatabasesAndUsers} from "./lambdas/create-databases-and-users";
import {Stack} from "aws-cdk-lib";
import {Construct} from "constructs";
import {LambdaStackProps} from "./lambda-stack-props";
import {Credentials} from "aws-cdk-lib/aws-rds";
import {Key} from "aws-cdk-lib/aws-kms";

export class LambdaStack extends Stack {
  readonly ckanCredentials: Credentials;
  constructor(scope: Construct, id: string, props: LambdaStackProps ) {
    super(scope, id, props);

    const secretsEncryptionKey = Key.fromLookup(this, 'EncryptionKey', {
      aliasName: `alias/secrets-encryption-key-${props.environment}`
    })

    const createDatabases = new CreateDatabasesAndUsers(this, 'create-databases-and-users', {
      env: props.env,
      envProps: props.envProps,
      ckanInstance: props.ckanInstance,
      ckanAdminCredentials: props.ckanAdminCredentials,
      vpc: props.vpc,
      environment: props.environment,
      secretsEncryptionKey: secretsEncryptionKey
    })

    this.ckanCredentials = Credentials.fromSecret(createDatabases.ckanSecret);
  }
}
