import {aws_ssm, Stack} from "aws-cdk-lib";
import {Construct} from "constructs";

import {EnvStackProps} from "./env-stack-props";

export class RestricteddataParameterStack extends Stack {
  readonly authSourceAddressesParameterName: string;

  constructor(scope: Construct, id: string, props: EnvStackProps ) {
    super(scope, id, props);

    this.authSourceAddressesParameterName = `/${props.environment}/restricteddata/auth_source_addresses`

    const authSourceAddresses = new aws_ssm.StringListParameter(this, 'authSourceAddresses', {
      stringListValue: ['127.0.0.1'],
      description: 'Authentication source IP address list',
      parameterName: this.authSourceAddressesParameterName
    })
  }
}
