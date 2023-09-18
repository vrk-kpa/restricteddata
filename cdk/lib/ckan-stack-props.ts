import {EcsStackProps} from "./ecs-stack-props";
import {CfnCacheCluster} from "aws-cdk-lib/aws-elasticache";
import {aws_ec2, aws_rds} from "aws-cdk-lib";

export interface CkanStackProps extends EcsStackProps {
  domainName: string,
  secondaryDomainName: string,
  redisCluster: CfnCacheCluster,
  redisSecurityGroup: aws_ec2.ISecurityGroup,
  ckanInstance: aws_rds.IDatabaseInstance,
  ckanInstanceCredentials: aws_rds.Credentials
  databaseSecurityGroup: aws_ec2.ISecurityGroup
}
