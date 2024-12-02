import {aws_ssm, Stack} from "aws-cdk-lib";
import {Construct} from "constructs";

import {EnvStackProps} from "./env-stack-props";

export class RestricteddataParameterStack extends Stack {
  readonly authSourceAddress: aws_ssm.IStringParameter;

  constructor(scope: Construct, id: string, props: EnvStackProps ) {
    super(scope, id, props);

    this.authSourceAddress = new aws_ssm.StringParameter(this, 'authSourceAddress', {
      stringValue: '127.0.0.1',
      description: 'Authentication source IP address',
      parameterName: `/${props.environment}/restricteddata/auth_source_address`
    })
  }
}
