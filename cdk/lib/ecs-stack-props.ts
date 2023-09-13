import {CommonStackProps} from "./common-stack-props";
import {EcsTaskDefinitionProps} from "./ecs-task-definition-props";

export interface EcsStackProps extends CommonStackProps {
  taskDef: EcsTaskDefinitionProps
}
