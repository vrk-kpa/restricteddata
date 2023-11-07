import {aws_ec2, aws_ecr, aws_ecs, aws_logs, aws_secretsmanager, aws_ssm, Duration, Stack} from "aws-cdk-lib";
import * as sd from 'aws-cdk-lib/aws-servicediscovery';
import {Construct} from "constructs";
import {CkanStackProps} from "./ckan-stack-props";
import {getRepositoryArn} from "./env-props";
import {Key} from "aws-cdk-lib/aws-kms";
import {Effect, PolicyStatement} from "aws-cdk-lib/aws-iam";

export class CkanStack extends Stack {
  constructor(scope: Construct, id: string, props: CkanStackProps) {
    super(scope, id, props);

    const pSysadminUser = aws_ssm.StringParameter.fromStringParameterAttributes(this, 'pSysadminUser', {
      parameterName: `/${props.environment}/registrydata/sysadmin_user`,
    });
    const pSysadminEmail = aws_ssm.StringParameter.fromStringParameterAttributes(this, 'pSysadminEmail', {
      parameterName: `/${props.environment}/registrydata/sysadmin_email`,
    });

    const pSmtpHost = aws_ssm.StringParameter.fromStringParameterAttributes(this, 'pSmtpHost', {
      parameterName: `/${props.environment}/smtp/server`,
    });

    const pSmtpFrom = aws_ssm.StringParameter.fromStringParameterAttributes(this, 'pSmtpFrom', {
      parameterName: `/${props.environment}/smtp/smtp_from`,
    });


    const ckanLogGroup = new aws_logs.LogGroup(this, 'ckanLogGroup', {
      logGroupName: `/${props.environment}/registrydata/ckan`,
    });

    const ckanRepo = aws_ecr.Repository.fromRepositoryArn(this, 'ckanRepo',
      getRepositoryArn(this, props.envProps.REGISTRY, props.envProps.REPOSITORY + '/ckan'));


    const ckanTaskDefinition = new aws_ecs.FargateTaskDefinition(this, 'ckanTaskDefinition', {
      cpu: props.taskDef.taskCpu,
      memoryLimitMiB: props.taskDef.taskMem,
    });

    const ckanPluginsDefault: string[] = [
      'fluent',
      'scheming_datasets',
      'scheming_groups',
    ];

    const ckanPlugins: string[] = [
      "dcat",
      "registrydata_pages",
      "pages",
      "markdown_editor",
      "registrydata",
      "activity",
      "text_view",
      "image_view"
    ]

    const ckanContainerEnv: {[key: string]: string} = {
      // env.ckan
      CKAN_SITE_URL: `https://${props.domainName}`,
      CKAN_SITE_ID: 'default',
      CKAN_PLUGINS_DEFAULT: ckanPluginsDefault.join(' '),
      CKAN_PLUGINS: ckanPlugins.join(' '),
      CKAN_WEBASSETS_PATH: '/srv/app/data/webassets',
      CKAN_MAX_RESOURCE_SIZE: '5000',
      CKAN_PROFILING_ENABLED: 'false',
      CKAN_LOG_LEVEL: 'INFO',
      CKAN_EXT_LOG_LEVEL: 'INFO',

      // .env
      CKAN_IMAGE_TAG: props.envProps.CKAN_IMAGE_TAG,
      REDIS_HOST: props.redisCluster.getAtt('RedisEndpoint.Address').toString(),
      REDIS_PORT: props.redisCluster.getAtt('RedisEndpoint.Port').toString(),
      REDIS_DB: '0',
      SOLR_HOST: `solr.${props.namespace.namespaceName}`,
      SOLR_PORT: '8983',
      SOLR_PATH: 'solr/ckan',
      NGINX_HOST: `nginx.${props.namespace.namespaceName}`,
      DB_CKAN_HOST: props.ckanInstance.instanceEndpoint.hostname,
      DB_CKAN: "ckan",
      DB_CKAN_USER: props.ckanInstanceCredentials.username,
      DOMAIN_NAME: props.domainName,
      SECONDARY_DOMAIN_NAME: props.secondaryDomainName,
      SITE_PROTOCOL: 'https',
      SMTP_HOST: pSmtpHost.stringValue,
      SMTP_FROM: pSmtpFrom.stringValue,
      SMTP_PROTOCOL: 'tls',
      SMTP_PORT: '587',
      CKAN_SYSADMIN_NAME: pSysadminUser.stringValue,
      CKAN_SYSADMIN_EMAIL: pSysadminEmail.stringValue,
      DEPLOY_ENVIRONMENT: props.environment,
    }

    const smtpSecrets = aws_secretsmanager.Secret.fromSecretNameV2(this, 'smtpSecrets',
      `/${props.environment}/smtp`)


    const secretEncryptionKey = Key.fromLookup(this, 'EncryptionKey', {
      aliasName: `alias/secrets-encryption-key-${props.environment}`
    })

    const beakerSecret = new aws_secretsmanager.Secret(this, 'beakerSecret', {
      encryptionKey: secretEncryptionKey,
      generateSecretString: {
        excludeCharacters: "%"
      }
    })

    const appUUIDSecret = new aws_secretsmanager.Secret(this, 'appUUIDSecret', {
      encryptionKey: secretEncryptionKey,
      generateSecretString: {
        excludeCharacters: "%"
      }
    })



    const ckanContainerSecrets: { [key: string]: aws_ecs.Secret; } = {
      // .env.ckan
      CKAN_BEAKER_SESSION_SECRET: aws_ecs.Secret.fromSecretsManager(beakerSecret),
      CKAN_APP_INSTANCE_UUID: aws_ecs.Secret.fromSecretsManager(appUUIDSecret),
      // .env
      DB_CKAN_PASS: aws_ecs.Secret.fromSecretsManager(props.ckanInstanceCredentials.secret!, 'password'),
      SMTP_USERNAME: aws_ecs.Secret.fromSecretsManager(smtpSecrets, 'username'),
      SMTP_PASS: aws_ecs.Secret.fromSecretsManager(smtpSecrets, 'password'),
      CKAN_SYSADMIN_PASSWORD: aws_ecs.Secret.fromSecretsManager(props.ckanSysAdminSecret),
    };

    ckanTaskDefinition.addToExecutionRolePolicy(new PolicyStatement({
      effect: Effect.ALLOW,
      actions: [
        "kms:Decrypt"
      ],
      resources: [
        secretEncryptionKey.keyArn
      ]
    }));

    props.ckanInstanceCredentials.secret!.grantRead(ckanTaskDefinition.executionRole!);




    const ckanContainer = ckanTaskDefinition.addContainer('ckan', {
      image: aws_ecs.ContainerImage.fromEcrRepository(ckanRepo, props.envProps.CKAN_IMAGE_TAG),
      environment: ckanContainerEnv,
      secrets: ckanContainerSecrets,
      logging: aws_ecs.LogDrivers.awsLogs({
        logGroup: ckanLogGroup,
        streamPrefix: 'ckan-service',
      }),
      healthCheck: {
        command: ['CMD-SHELL', 'curl --fail http://localhost:5000/api/3/action/status_show --user-agent "docker-healthcheck" || exit 1'],
        interval: Duration.seconds(15),
        timeout: Duration.seconds(5),
        retries: 5,
        startPeriod: Duration.seconds(300),
      },
      linuxParameters: new aws_ecs.LinuxParameters(this, 'ckanContainerLinuxParams', {
        initProcessEnabled: true,
      }),
    });

    ckanContainer.addPortMappings({
      containerPort: 5000,
      protocol: aws_ecs.Protocol.TCP,
    });

     const ckanService = new aws_ecs.FargateService(this, 'ckanService', {
      platformVersion: aws_ecs.FargatePlatformVersion.VERSION1_4,
      cluster: props.cluster,
      taskDefinition: ckanTaskDefinition,
      minHealthyPercent: 50,
      maxHealthyPercent: 200,
      cloudMapOptions: {
        cloudMapNamespace: props.namespace,
        dnsRecordType: sd.DnsRecordType.A,
        dnsTtl: Duration.minutes(1),
        name: 'ckan',
        container: ckanContainer,
        containerPort: 5000
      },
      enableExecuteCommand: true,
    });

    ckanService.connections.allowTo(props.databaseSecurityGroup, aws_ec2.Port.tcp(5432), 'RDS connection (ckan)');
    ckanService.connections.allowTo(props.redisSecurityGroup, aws_ec2.Port.tcp(6379), 'Redis connection (ckan)');
    ckanService.connections.allowTo(props.solrService, aws_ec2.Port.tcp(8983), 'Solr connection (ckan)')
    ckanService.connections.allowFrom(props.nginxService.service, aws_ec2.Port.tcp(5000), 'HTTP connection (ckan)' )

    const ckanServiceAsg = ckanService.autoScaleTaskCount({
      minCapacity: props.taskDef.taskMinCapacity,
      maxCapacity: props.taskDef.taskMaxCapacity,
    });

    ckanServiceAsg.scaleOnCpuUtilization('ckanServiceAsgPolicy', {
      targetUtilizationPercent: 50,
      scaleInCooldown: Duration.seconds(60),
      scaleOutCooldown: Duration.seconds(60),
    });

    ckanServiceAsg.scaleOnMemoryUtilization('ckanServiceAsgPolicyMem', {
      targetUtilizationPercent: 80,
      scaleInCooldown: Duration.seconds(60),
      scaleOutCooldown: Duration.seconds(60),
    });

    const ckanCronTaskDefinition = new aws_ecs.FargateTaskDefinition(this, 'ckanTaskDefinition', {
      cpu: props.cronTaskDef.taskCpu,
      memoryLimitMiB: props.cronTaskDef.taskMem,
    });
    ckanCronTaskDefinition.addToExecutionRolePolicy(new PolicyStatement({
      effect: Effect.ALLOW,
      actions: [
        "kms:Decrypt"
      ],
      resources: [
        secretEncryptionKey.keyArn
      ]
    }));

    props.ckanInstanceCredentials.secret!.grantRead(ckanCronTaskDefinition.executionRole!);

    const ckanCronLogGroup = new aws_logs.LogGroup(this, 'ckanCronLogGroup', {
      logGroupName: `/${props.environment}/registrydata/ckanCron`,
    });

    const ckanCronContainer = ckanCronTaskDefinition.addContainer('ckanCron', {
      image: aws_ecs.ContainerImage.fromEcrRepository(ckanRepo, props.envProps.CKAN_IMAGE_TAG),
      environment: ckanContainerEnv,
      secrets: ckanContainerSecrets,
      entryPoint: ['/srv/app/scripts/entrypoint_cron.sh'],
      logging: aws_ecs.LogDrivers.awsLogs({
        logGroup: ckanCronLogGroup,
        streamPrefix: 'ckan-cron-service',
      }),
      healthCheck: {
        command: ['CMD-SHELL', 'ps aux | grep -o "[c]rond -f" && ps aux | grep -o "[s]upervisord --configuration"'],
        interval: Duration.seconds(15),
        timeout: Duration.seconds(5),
        retries: 5,
        startPeriod: Duration.seconds(300),
      },
      linuxParameters: new aws_ecs.LinuxParameters(this, 'ckanContainerLinuxParams', {
        initProcessEnabled: true,
      }),
    });

    const ckanCronService = new aws_ecs.FargateService(this, 'ckanCronService', {
      platformVersion: aws_ecs.FargatePlatformVersion.VERSION1_4,
      cluster: props.cluster,
      taskDefinition: ckanCronTaskDefinition,
      desiredCount: 1,
      minHealthyPercent: 0,
      maxHealthyPercent: 100,
      enableExecuteCommand: true,
    });

    ckanCronService.connections.allowTo(props.databaseSecurityGroup, aws_ec2.Port.tcp(5432), 'RDS connection (ckanCron)');
    ckanCronService.connections.allowTo(props.redisSecurityGroup, aws_ec2.Port.tcp(6379), 'Redis connection (ckanCron)');
    ckanCronService.connections.allowTo(props.solrService, aws_ec2.Port.tcp(8983), 'Solr connection (ckanCron)')
  }
}
