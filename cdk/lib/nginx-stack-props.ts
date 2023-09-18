import {EcsStackProps} from "./ecs-stack-props";
import {aws_certificatemanager, aws_elasticloadbalancingv2, aws_route53} from "aws-cdk-lib";

export interface NginxStackProps extends EcsStackProps {
  allowRobots: string,
  certificate: aws_certificatemanager.ICertificate,
  loadBalancer: aws_elasticloadbalancingv2.IApplicationLoadBalancer,
  zone: aws_route53.IPublicHostedZone,
  domainName: string,
  secondaryDomainName: string,
  fqdn: string,
  secondaryFqdn: string,

}
