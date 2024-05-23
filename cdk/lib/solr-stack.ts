import {aws_ec2, aws_ecr, aws_ecs, aws_logs, Duration, Stack} from "aws-cdk-lib";
import {Construct} from "constructs";
import * as sd from 'aws-cdk-lib/aws-servicediscovery';
import * as efs from 'aws-cdk-lib/aws-efs';
import {EcsStackProps} from "./ecs-stack-props";
import {getRepositoryArn} from "./env-props";

export class SolrStack extends Stack {
  readonly solrService: aws_ecs.FargateService;
  constructor(scope: Construct, id: string, props: EcsStackProps) {
    super(scope, id, props);

    const solrLogGroup = new aws_logs.LogGroup(this, 'solrLogGroup', {
      logGroupName: `/${props.environment}/restricteddata/solr`,
    });

    const solrRepo = aws_ecr.Repository.fromRepositoryArn(this, 'solrRepo',
      getRepositoryArn(this, props.envProps.REGISTRY, props.envProps.REPOSITORY + '/solr'));


    const solrFsDataAccessPoint = props.fileSystem!.addAccessPoint('solrFsDataAccessPoint', {
      path: '/solr_data',
      createAcl: {
        ownerGid: '8983',
        ownerUid: '8983',
        permissions: '0755',
      },
      posixUser: {
        gid: '8983',
        uid: '8983',
      },
    });

    const solrTaskDef = new aws_ecs.FargateTaskDefinition(this, 'solrTaskDef', {
      cpu: props.taskDef.taskCpu,
      memoryLimitMiB: props.taskDef.taskMem,
      volumes: [
        {
          name: 'solr_data',
          efsVolumeConfiguration: {
            fileSystemId: props.fileSystem!.fileSystemId,
            authorizationConfig: {
              accessPointId: solrFsDataAccessPoint.accessPointId,
            },
            transitEncryption: 'ENABLED',
          },
        }
      ],
    });


    const solrContainer = solrTaskDef.addContainer('solr', {
      image: aws_ecs.ContainerImage.fromEcrRepository(solrRepo, props.envProps.SOLR_IMAGE_TAG),
      logging: aws_ecs.LogDrivers.awsLogs({
        logGroup: solrLogGroup,
        streamPrefix: 'solr-service',
      }),
      healthCheck: {
        command: ['CMD-SHELL', 'curl --fail -s http://localhost:8983/solr/ckan/admin/ping?wt=json | grep -o "OK"'],
        interval: Duration.seconds(15),
        timeout: Duration.seconds(5),
        retries: 5,
        startPeriod: Duration.seconds(15),
      },
    });

    solrContainer.addPortMappings({
      containerPort: 8983,
      protocol: aws_ecs.Protocol.TCP,
    });

    solrContainer.addMountPoints({
      containerPath: '/var/solr/data/ckan/data',
      readOnly: false,
      sourceVolume: 'solr_data',
    });

    this.solrService = new aws_ecs.FargateService(this, 'solrService', {
      platformVersion: aws_ecs.FargatePlatformVersion.VERSION1_4,
      cluster: props.cluster,
      taskDefinition: solrTaskDef,
      desiredCount: 1,
      minHealthyPercent: 0,
      maxHealthyPercent: 100,
      cloudMapOptions: {
        cloudMapNamespace: props.namespace,
        dnsRecordType: sd.DnsRecordType.A,
        dnsTtl: Duration.minutes(1),
        name: 'solr',
        container: solrContainer,
        containerPort: 8983
      },
    });

    if (props.fileSystem){
      // not sure if needed
      //solrService.connections.allowFrom(props.fileSystem, aws_ec2.Port.tcp(2049), 'EFS connection (solr)');
      this.solrService.connections.allowTo(props.fileSystem, aws_ec2.Port.tcp(2049), 'EFS connection (solr)');
    }


    const solrServiceAsg = this.solrService.autoScaleTaskCount({
      minCapacity: props.taskDef.taskMinCapacity,
      maxCapacity: props.taskDef.taskMaxCapacity,
    });



  }
}
