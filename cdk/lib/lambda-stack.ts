
import {CreateDatabasesAndUsers} from "./lambdas/create-databases-and-users";
import {Stack} from "aws-cdk-lib";
import {Construct} from "constructs";
import {LambdaStackProps} from "./lambda-stack-props";
import {Credentials} from "aws-cdk-lib/aws-rds";
import {Key} from "aws-cdk-lib/aws-kms";
import { SendToZulip } from "./send-to-zulip";
import { NodejsFunction } from "aws-cdk-lib/aws-lambda-nodejs";

export class LambdaStack extends Stack {
  readonly ckanCredentials: Credentials;
  readonly sendToZulipLambda: NodejsFunction;
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

    const sendToZulip = new SendToZulip(this, 'send-to-zulip', {
      zulipApiUser: 'avoindata-bot@turina.dvv.fi',
      zulipApiUrl: 'turina.dvv.fi',
      zulipStream: 'DGA',
      zulipTopic: 'Container restarts',
      envProps: props.envProps,
      env: props.env,
      environment: props.environment,
      vpc: props.vpc
    });
    this.sendToZulipLambda = sendToZulip.lambda;
  }
}
