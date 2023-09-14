import {CommonStackProps} from "./common-stack-props";
import {EcsTaskDefinitionProps} from "./ecs-task-definition-props";
import {aws_ecs, aws_servicediscovery} from "aws-cdk-lib";

export interface EcsStackProps extends CommonStackProps {
  taskDef: EcsTaskDefinitionProps,
  domainName: string,
  secondaryDomainName: string,
  fqdn: string,
  secondaryFqdn: string,
  namespace: aws_servicediscovery.INamespace,
  cluster: aws_ecs.ICluster
}
