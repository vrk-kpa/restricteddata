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
  highPriorityRateLimitParameterName: string,
  rateLimitParameterName: string,
  managedRulesParameterName: string,
  wafAutomationArnParameterName: string,
  snsTopicArnParameterName: string,
  evaluationPeriodParameterName: string

}
