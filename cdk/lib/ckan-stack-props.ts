import {EcsStackProps} from "./ecs-stack-props";
import {EcsTaskDefinitionProps} from "./ecs-task-definition-props";
import {CfnCacheCluster} from "aws-cdk-lib/aws-elasticache";
import {aws_ec2, aws_ecs, aws_ecs_patterns, aws_rds, aws_secretsmanager} from "aws-cdk-lib";

export interface CkanStackProps extends EcsStackProps {
  domainName: string,
  secondaryDomainName: string,
  redisCluster: CfnCacheCluster,
  redisSecurityGroup: aws_ec2.ISecurityGroup,
  ckanInstance: aws_rds.IDatabaseInstance,
  ckanInstanceCredentials: aws_rds.Credentials
  ckanSysAdminSecret: aws_secretsmanager.ISecret,
  databaseSecurityGroup: aws_ec2.ISecurityGroup,
  solrService: aws_ecs.FargateService,
  nginxService: aws_ecs_patterns.ApplicationLoadBalancedFargateService,
  cronTaskDef: EcsTaskDefinitionProps,
  analyticsEnabled: boolean,
  matomoSiteId: number | undefined,
  matomoDomain: string | undefined,
  matomoScriptDomain: string | undefined,
  sentryTracesSampleRate: string,
  sentryProfilesSampleRate: string
}
