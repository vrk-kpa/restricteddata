
import {CreateDatabasesAndUsers} from "./create-databases-and-users";
import {Stack} from "aws-cdk-lib";
import {Construct} from "constructs";
import {LambdaStackProps} from "./lambda-stack-props";
import {Credentials} from "aws-cdk-lib/aws-rds";

export class LambdaStack extends Stack {
  readonly ckanCredentials: Credentials;
  constructor(scope: Construct, id: string, props: LambdaStackProps ) {
    super(scope, id, props);
    const createDatabases = new CreateDatabasesAndUsers(this, 'create-databases-and-users', {
      env: props.env,
      ckanInstance: props.ckanInstance,
      ckanAdminCredentials: props.ckanAdminCredentials,
      vpc: props.vpc,
      environment: props.environment,
      databaseSecretsEncryptionKey: props.databaseSecretsEncryptionKey
    })

    this.ckanCredentials = Credentials.fromSecret(createDatabases.ckanSecret);
  }
}