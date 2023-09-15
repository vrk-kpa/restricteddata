import {
  aws_ecr,
  aws_ecs,
  aws_ecs_patterns,
  aws_elasticloadbalancingv2,
  aws_logs, aws_route53, aws_route53_targets,
  aws_servicediscovery, Duration,
  Stack
} from "aws-cdk-lib";
import {Construct} from "constructs";
import {getRepositoryArn} from "./env-props";
import {NginxStackProps} from "./nginx-stack-props";


export class NginxStack extends Stack {

  constructor(scope: Construct, id: string, props: NginxStackProps) {
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
        NAMESERVER: "169.254.169.253",
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


    const nginxService = new aws_ecs_patterns.ApplicationLoadBalancedFargateService(this, 'nginxService', {
      cluster: props.cluster,
      cloudMapOptions: {
        cloudMapNamespace: props.namespace,
        dnsRecordType: aws_servicediscovery.DnsRecordType.A,
        dnsTtl: Duration.minutes(1),
        name: 'nginx',
        container: nginxContainer,
        containerPort: 80,
      },
      publicLoadBalancer: true,
      protocol: aws_elasticloadbalancingv2.ApplicationProtocol.HTTPS,
      certificate: props.certificate,
      redirectHTTP: false,
      platformVersion: aws_ecs.FargatePlatformVersion.VERSION1_4,
      taskDefinition: nginxTaskDefinition,
      minHealthyPercent: 50,
      maxHealthyPercent: 200,
      loadBalancer: props.loadBalancer,
      openListener: false
    });


    nginxService.targetGroup.configureHealthCheck({
      path: '/health',
      healthyHttpCodes: '200',
    });

    nginxService.targetGroup.setAttribute('deregistration_delay.timeout_seconds', '60');

    const nginxServiceAsg = nginxService.service.autoScaleTaskCount({
      minCapacity: props.taskDef.taskMinCapacity,
      maxCapacity: props.taskDef.taskMaxCapacity,
    });

    nginxServiceAsg.scaleOnCpuUtilization('nginxServiceAsgPolicy', {
      targetUtilizationPercent: 50,
      scaleInCooldown: Duration.seconds(60),
      scaleOutCooldown: Duration.seconds(60),
    });


    const rootRecord = new aws_route53.ARecord(this, 'subDomainRecord', {
      zone: props.zone,
      target: aws_route53.RecordTarget.fromAlias(new aws_route53_targets.LoadBalancerTarget(props.loadBalancer))
    })
  }
}

