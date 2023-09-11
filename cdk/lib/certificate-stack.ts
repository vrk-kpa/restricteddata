import {Stack, aws_certificatemanager as acm} from "aws-cdk-lib";
import {Construct} from "constructs";
import {CertificateStackProps} from "./certificate-stack-props";

export class CertificateStack extends Stack {
    readonly certificate: acm.ICertificate;
    constructor(scope: Construct, id: string, props: CertificateStackProps) {
        super(scope, id, props);

        this.certificate = new acm.Certificate(this, 'Certificate', {
            domainName: props.zone.zoneName,
            validation: acm.CertificateValidation.fromDns(props.zone)
        })
    }
}