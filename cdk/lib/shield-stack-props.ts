import {aws_elasticloadbalancingv2, aws_ssm} from "aws-cdk-lib";

import {EnvStackProps} from "./env-stack-props";

export interface ShieldStackProps extends EnvStackProps {
  loadBalancer: aws_elasticloadbalancingv2.IApplicationLoadBalancer,
  bannedIpsRequestSamplingEnabled: boolean,
  requestSampleAllTrafficEnabled: boolean,
  highPriorityRequestSamplingEnabled: boolean,
  rateLimitRequestSamplingEnabled: boolean
  bannedIpListParameterName: string,
  whitelistedIpListParameterName: string,
  highPriorityCountryCodeListParameterName: string,
  highPriorityRateLimit: aws_ssm.IStringParameter,
  rateLimit: aws_ssm.IStringParameter,
  managedRulesParameterName: string,
  wafAutomationArn: aws_ssm.IStringParameter,
  snsTopicArn: aws_ssm.IStringParameter,
  evaluationPeriod: aws_ssm.IStringParameter

}
