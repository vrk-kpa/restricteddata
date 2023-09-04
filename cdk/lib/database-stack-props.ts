import {CommonStackProps} from "./common-stack-props";
import {aws_kms} from "aws-cdk-lib";

export interface DatabaseStackProps extends CommonStackProps {
    databaseEncryptionKey: aws_kms.IKey;
    multiAz: boolean;
}