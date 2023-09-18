import {CommonStackProps} from "./common-stack-props";
import {EcsTaskDefinitionProps} from "./ecs-task-definition-props";
import {aws_ecs, aws_efs, aws_servicediscovery} from "aws-cdk-lib";

export interface EcsStackProps extends CommonStackProps {
  taskDef: EcsTaskDefinitionProps,
  namespace: aws_servicediscovery.INamespace,
  cluster: aws_ecs.ICluster,
  fileSystem?: aws_efs.FileSystem
}
