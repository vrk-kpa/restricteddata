import {aws_ecr, aws_ecs, aws_logs, Stack} from "aws-cdk-lib";
import {Construct} from "constructs";
import {CommonStackProps} from "./common-stack-props";
import {EcsStackProps} from "./ecs-stack-props";
import {getRepositoryArn} from "./env-props";


export class NginxStack extends Stack {

  constructor(scope: Construct, id: string, props: EcsStackProps) {
    super(scope, id, props);

    const nginxLogGroup = new aws_logs.LogGroup(this, 'nginxLogGroup', {
      logGroupName: `/${props.environment}/registrydata/nginx`,
    });

    const nginxRepo = aws_ecr.Repository.fromRepositoryArn(this, 'nginxRepo',
      getRepositoryArn(this, props.envProps.REGISTRY, props.envProps.REPOSITORY + '/nginx'));


    const nginxTaskDefinition = new aws_ecs.FargateTaskDefinition(this, "nginxTaskDef", {
      cpu: props.taskDef.taskCpu,
      memoryLimitMiB: props.taskDef.taskMem
    })

    // define nginx content security policies
    const nginxCspDefaultSrc: string[] = [];
    const nginxCspScriptSrc: string[] = [];
    const nginxCspStyleSrc: string[] = [];
    const nginxCspFrameSrc: string[] = [];


    const nginxContainer = nginxTaskDefinition.addContainer('nginx', {
      image: aws_ecs.ContainerImage.fromEcrRepository(nginxRepo, props.envProps.NGINX_IMAGE_TAG),
      environment: {
        // .env.nginx
        NGINX_ROOT: '/var/www/html',
        NGINX_MAX_BODY_SIZE: '5000M',
        NGINX_EXPIRES: '1h',
        NGINX_CSP_DEFAULT_SRC: nginxCspDefaultSrc.join(' '),
        NGINX_CSP_SCRIPT_SRC: nginxCspScriptSrc.join(' '),
        NGINX_CSP_STYLE_SRC: nginxCspStyleSrc.join(' '),
        NGINX_CSP_FRAME_SRC: nginxCspFrameSrc.join(' '),

        // .env
        NGINX_PORT: "80",
        DOMAIN_NAME: props.domainName,
        SECONDARY_DOMAIN_NAME: props.secondaryDomainName,
        BASE_DOMAIN_NAME: props.fqdn,
        SECONDARY_BASE_DOMAIN_NAME: props.secondaryFqdn,
        NAMESERVER: pNameserver.stringValue,
        CKAN_HOST: `ckan.${props.namespace.namespaceName}`,
        CKAN_PORT: '5000',
        NGINX_ROBOTS_ALLOW: props.allowRobots,
      },
      logging: aws_ecs.LogDrivers.awsLogs({
        logGroup: nginxLogGroup,
        streamPrefix: 'nginx-service'
      })
    })

    nginxContainer.addPortMappings({
      containerPort: 80,
      protocol: aws_ecs.Protocol.TCP,
    });



  }
}

