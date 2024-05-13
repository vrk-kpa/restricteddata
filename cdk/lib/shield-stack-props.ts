import {aws_elasticloadbalancingv2} from "aws-cdk-lib";

import {EnvStackProps} from "./env-stack-props";

export interface ShieldStackProps extends EnvStackProps {
  loadBalancer: aws_elasticloadbalancingv2.IApplicationLoadBalancer,
  bannedIpsRequestSamplingEnabled: boolean,
  requestSampleAllTrafficEnabled: boolean,
  highPriorityRequestSamplingEnabled: boolean,
  rateLimitRequestSamplingEnabled: boolean
}
