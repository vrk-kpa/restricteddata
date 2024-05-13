import {EnvProps} from "./env-props";
import {NetworkStackProps} from "./network-stack-props";

export interface CommonStackProps extends NetworkStackProps {
  envProps: EnvProps;
}
