import {aws_kms, Stack, StackProps} from "aws-cdk-lib";
import {Construct} from "constructs";
import {EnvStackProps} from "./env-stack-props";

export class KmsKeyStack extends Stack {
    readonly databaseEncryptionKey: aws_kms.IKey;

    constructor(scope: Construct, id: string, props: EnvStackProps) {
        super(scope, id, props);

        this.databaseEncryptionKey = new aws_kms.Key(this, 'databaseEncryptionKey', {
            alias: `database-encryption-key-${props.environment}`
        })

        const secretsEncryptionKey = new aws_kms.Key(this, 'secretsEncryptionKey', {
          alias: `secrets-encryption-key-${props.environment}`
        })
    }

}
