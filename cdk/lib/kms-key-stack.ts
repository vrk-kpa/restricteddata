import {aws_kms, Stack, StackProps} from "aws-cdk-lib";
import {Construct} from "constructs";

export class KmsKeyStack extends Stack {
    readonly databaseEncryptionKey: aws_kms.IKey;
    constructor(scope: Construct, id: string, props: StackProps) {
        super(scope, id, props);

        this.databaseEncryptionKey = new aws_kms.Key(this, 'databaseEncryptionKey', {

        })

    }

}