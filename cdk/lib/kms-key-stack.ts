import {aws_kms, Stack, StackProps} from "aws-cdk-lib";
import {Construct} from "constructs";
import {CommonStackProps} from "./common-stack-props";

export class KmsKeyStack extends Stack {
    readonly databaseEncryptionKey: aws_kms.IKey;
  
    constructor(scope: Construct, id: string, props: CommonStackProps) {
        super(scope, id, props);

        this.databaseEncryptionKey = new aws_kms.Key(this, 'databaseEncryptionKey', {

        })

        const secretsEncryptionKey = new aws_kms.Key(this, 'secretsEncryptionKey', {
          alias: `secrets-encryption-key-${props.environment}`
        })
    }

}