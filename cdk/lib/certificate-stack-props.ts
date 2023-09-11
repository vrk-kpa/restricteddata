import {aws_route53, StackProps} from "aws-cdk-lib";

export interface CertificateStackProps extends StackProps {
    zone: aws_route53.IPublicHostedZone;
}
