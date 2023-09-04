import {StackProps} from "aws-cdk-lib";
import {IVpc} from "aws-cdk-lib/aws-ec2";

export interface CommonStackProps extends StackProps {
    environment: string;
    vpc: IVpc;
}