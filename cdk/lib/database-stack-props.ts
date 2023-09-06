import {CommonStackProps} from "./common-stack-props";
import {aws_kms} from "aws-cdk-lib";

export interface DatabaseStackProps extends CommonStackProps {
    multiAz: boolean;
}