#!/usr/bin/env node
import 'source-map-support/register';
import * as dotenv from 'dotenv';
import * as cdk from 'aws-cdk-lib';
import { DomainStack } from '../lib/domain-stack';
import {VpcStack} from "../lib/vpc-stack";
import {DatabaseStack} from "../lib/database-stack";
import {KmsKeyStack} from "../lib/kms-key-stack";
import {LambdaStack} from "../lib/lambda-stack"
import {LoadBalancerStack} from "../lib/load-balancer-stack";
import {SubDomainStack} from "../lib/sub-domain-stack";
import {BackupStack} from "../lib/backup-stack";
import {CertificateStack} from "../lib/certificate-stack";
import {EnvProps, parseEnv} from "../lib/env-props";
import {EcsClusterStack} from "../lib/ecs-cluster-stack";
import {NginxStack} from "../lib/nginx-stack";
import {SolrStack} from "../lib/solr-stack";
import {FileSystemStack} from "../lib/filesystem-stack";
import {CkanStack} from "../lib/ckan-stack";
import {ShieldParameterStack} from "../lib/shield-parameter-stack";
import {ShieldStack} from "../lib/shield-stack";
import {MonitoringStack} from '../lib/monitoring-stack';
import { RestricteddataParameterStack } from '../lib/restricteddata-parameter-stack';

const app = new cdk.App();

const prodStackProps = {
  account: '157248445006',
  region: 'eu-north-1',
  environment: "prod",
  domainName: "suojattudata.fi",
  secondaryDomainName: "suojattudata.suomi.fi",
  fqdn: "suojattudata.fi",
  secondaryFqdn: "suomi.fi"
}

const devStackProps = {
  account: '332833619545',
  region: 'eu-north-1',
  environment: "dev",
  domainName: "dev.suojattudata.fi",
  secondaryDomainName: "dev.suojattudata.suomi.fi",
  fqdn: "suojattudata.fi",
  secondaryFqdn: "suomi.fi"
}


// load .env file, shared with docker setup
// mainly for ECR repo and image tag information
dotenv.config({
  path: '../docker/.env',
});


const envProps: EnvProps = {
  // docker
  REGISTRY: parseEnv('REGISTRY'),
  REPOSITORY: parseEnv('REPOSITORY'),
  // opendata images
  CKAN_IMAGE_TAG: parseEnv('CKAN_IMAGE_TAG'),
  SOLR_IMAGE_TAG: parseEnv('SOLR_IMAGE_TAG'),
  NGINX_IMAGE_TAG: parseEnv('NGINX_IMAGE_TAG'),
  // 3rd party image
};

// Common

const DomainStackProd = new DomainStack(app, 'DomainStack-prod', {
  env: {
    account: prodStackProps.account,
    region: prodStackProps.region
  },
  crossAccountId: devStackProps.account
});

// Dev

const VpcStackDev = new VpcStack(app, 'VpcStack-dev', {
  env: {
    account: devStackProps.account,
    region: devStackProps.region
  },
  maxAzs: 2
})


const KmsKeyStackDev = new KmsKeyStack(app, 'KmsKeyStack-dev', {
  env: {
    account: devStackProps.account,
    region: devStackProps.region
  },
  environment: devStackProps.environment,
})

const BackupStackDev = new BackupStack(app, 'BackupStack-dev', {
  env: {
    account: devStackProps.account,
    region: devStackProps.region,
  },
  environment: devStackProps.environment,
  importVault: true,
  backups: true
})

const DatabaseStackDev = new DatabaseStack(app, 'DatabaseStack-dev', {
  env: {
    account: devStackProps.account,
    region: devStackProps.region
  },
  environment: devStackProps.environment,
  vpc: VpcStackDev.vpc,
  multiAz: false,
  backups: true,
  backupPlan: BackupStackDev.backupPlan,
  cacheNodeType: 'cache.t3.micro',
  numCacheNodes: 1,
  terminationProtection: true,
  restoreFromSnapshot: true,
  snapshotIdentifier: 'pre-subnet-reduction'
})

const LoadBalancerStackDev = new LoadBalancerStack(app, 'LoadBalancerStack-dev', {
  env: {
    account: devStackProps.account,
    region: devStackProps.region
  },
  environment: devStackProps.environment,
  vpc: VpcStackDev.vpc
})

const LambdaStackDev = new LambdaStack(app, 'LambdaStack-dev', {
  env: {
    account: devStackProps.account,
    region: devStackProps.region,
  },
  environment: devStackProps.environment,
  ckanInstance: DatabaseStackDev.ckanInstance,
  ckanAdminCredentials: DatabaseStackDev.ckanAdminCredentials,
  vpc: VpcStackDev.vpc,
})

const SubDomainStackDev = new SubDomainStack(app, 'SubDomainStack-dev', {
  env: {
    account: devStackProps.account,
    region: devStackProps.region,
  },
  prodAccountId: prodStackProps.account,
  subDomainName: "dev"
})

const CertificateStackDev = new CertificateStack(app, 'CertificateStack-dev', {
  env: {
    account: devStackProps.account,
    region: devStackProps.region,
  },
  zone: SubDomainStackDev.subZone,
  newZone: SubDomainStackDev.newSubZone
})

const EcsClusterStackDev = new EcsClusterStack(app, 'EcsClusterStack-dev', {
  env: {
    account: devStackProps.account,
    region: devStackProps.region,
  },
  environment: devStackProps.environment,
  vpc: VpcStackDev.vpc
})

const FileSystemStackDev = new FileSystemStack(app, 'FilesystemStack-dev', {
  env: {
    account: devStackProps.account,
    region: devStackProps.region,
  },
  environment: devStackProps.environment,
  vpc: VpcStackDev.vpc,
  terminationProtection: true
})

const RestricteddataParameterStackDev = new RestricteddataParameterStack(app, 'RestricteddataParameterStack-dev', {
  env: {
    account: devStackProps.account,
    region: devStackProps.region,
  },
  environment: devStackProps.environment,
})


const NginxStackDev = new NginxStack(app, 'NginxStack-dev', {
  env: {
    account: devStackProps.account,
    region: devStackProps.region,
  },
  envProps: envProps,
  environment: devStackProps.environment,
  vpc: VpcStackDev.vpc,
  allowRobots: "false",
  certificate: CertificateStackDev.certificate,
  newCertificate: CertificateStackDev.newCertificate,
  cluster: EcsClusterStackDev.cluster,
  namespace: EcsClusterStackDev.namespace,
  domainName: devStackProps.domainName,
  fqdn: devStackProps.fqdn,
  secondaryDomainName: devStackProps.secondaryDomainName,
  secondaryFqdn: devStackProps.secondaryFqdn,
  loadBalancer: LoadBalancerStackDev.loadBalancer,
  zone: SubDomainStackDev.subZone,
  newZone: SubDomainStackDev.newSubZone,
  taskDef: {
    taskCpu: 256,
    taskMem: 512,
    taskMinCapacity: 1,
    taskMaxCapacity: 1
  },
  authSourceAddressesParameterName: RestricteddataParameterStackDev.authSourceAddressesParameterName
})

const SolrStackDev = new SolrStack(app, 'SolrStack-dev', {
  env: {
    account: devStackProps.account,
    region: devStackProps.region,
  },
  envProps: envProps,
  environment: devStackProps.environment,
  cluster: EcsClusterStackDev.cluster,
  namespace: EcsClusterStackDev.namespace,
  taskDef: {
    taskCpu: 256,
    taskMem: 1024,
    taskMinCapacity: 1,
    taskMaxCapacity: 1
  },
  vpc: VpcStackDev.vpc,
  fileSystem: FileSystemStackDev.solrFs
})

const CkanStackDev = new CkanStack(app, 'CkanStack-dev', {
  env: {
    account: devStackProps.account,
    region: devStackProps.region,
  },
  envProps: envProps,
  environment: devStackProps.environment,
  ckanInstance: DatabaseStackDev.ckanInstance,
  ckanInstanceCredentials: LambdaStackDev.ckanCredentials,
  ckanSysAdminSecret: DatabaseStackDev.ckanSysAdminSecret,
  cluster: EcsClusterStackDev.cluster,
  databaseSecurityGroup: DatabaseStackDev.databaseSecurityGroup,
  domainName: devStackProps.domainName,
  namespace: EcsClusterStackDev.namespace,
  redisCluster: DatabaseStackDev.redisCluster,
  redisSecurityGroup: DatabaseStackDev.redisSecurityGroup,
  solrService: SolrStackDev.solrService,
  nginxService: NginxStackDev.nginxService,
  secondaryDomainName: devStackProps.secondaryDomainName,
  fileSystem: FileSystemStackDev.ckanFs,
  taskDef: {
    taskCpu: 512,
    taskMem: 1024,
    taskMinCapacity: 1,
    taskMaxCapacity: 1
  },
  cronTaskDef: {
    taskCpu: 256,
    taskMem: 1024,
    taskMinCapacity: 1,
    taskMaxCapacity: 1
  },
  vpc: VpcStackDev.vpc,
  analyticsEnabled: true,
  matomoSiteId: 47,
  matomoDomain: "suomi.matomo.cloud",
  matomoScriptDomain: "//cdn.matomo.cloud/suomi.matomo.cloud/",
  sentryTracesSampleRate: "1.0",
  sentryProfilesSampleRate: "1.0"
})

const ShieldParameterStackDev = new ShieldParameterStack(app, 'ShieldParameterStack-dev', {
  env: {
    account: devStackProps.account,
    region: devStackProps.region,
  },
  environment: devStackProps.environment,
})

const ShieldStackDev = new ShieldStack(app, 'ShieldStack-dev', {
  env: {
    account: devStackProps.account,
    region: devStackProps.region,
  },
  environment: devStackProps.environment,
  loadBalancer: LoadBalancerStackDev.loadBalancer,
  rateLimitRequestSamplingEnabled: false,
  highPriorityRequestSamplingEnabled: false,
  bannedIpsRequestSamplingEnabled: false,
  requestSampleAllTrafficEnabled: false,
  bannedIpListParameterName: ShieldParameterStackDev.bannedIpListParameterName,
  whitelistedIpListParameterName: ShieldParameterStackDev.whitelistedIpListParameterName,
  highPriorityCountryCodeListParameterName: ShieldParameterStackDev.highPriorityCountryCodeListParameterName,
  highPriorityRateLimitParameterName: ShieldParameterStackDev.highPriorityRateLimitParameterName,
  rateLimitParameterName: ShieldParameterStackDev.rateLimitParameterName,
  managedRulesParameterName: ShieldParameterStackDev.managedRulesParameterName,
  snsTopicArnParameterName: ShieldParameterStackDev.snsTopicArnParameterName,
  wafAutomationArnParameterName: ShieldParameterStackDev.wafAutomationArnParameterName,
  evaluationPeriodParameterName: ShieldParameterStackDev.evaluationPeriodParameterName
})

const MonitoringStackDev = new MonitoringStack(app, 'MonitoringStack-dev', {
  sendToZulipLambda: LambdaStackDev.sendToZulipLambda,
  env: {
    account: devStackProps.account,
    region: devStackProps.region,
  },
});

// Production


const VpcStackProd = new VpcStack(app, 'VpcStack-prod', {
  env: {
    account: prodStackProps.account,
    region: prodStackProps.region
  },
  maxAzs: 3
})

const KmsKeyStackProd = new KmsKeyStack(app, 'KmsKeyStack-prod', {
  env: {
    account: prodStackProps.account,
    region: prodStackProps.region
  },
  environment: prodStackProps.environment
})

const BackupStackProd = new BackupStack(app, 'BackupStack-prod', {
  env: {
    account: prodStackProps.account,
    region: prodStackProps.region,
  },
  environment: prodStackProps.environment,
  importVault: false,
  backups: true
})

const DatabaseStackProd = new DatabaseStack(app, 'DatabaseStack-prod', {
  env: {
    account: prodStackProps.account,
    region: prodStackProps.region
  },
  environment: prodStackProps.environment,
  vpc: VpcStackProd.vpc,
  multiAz: false,
  backups: true,
  backupPlan: BackupStackProd.backupPlan,
  cacheNodeType: 'cache.t3.micro',
  numCacheNodes: 1,
  terminationProtection: true,
  restoreFromSnapshot: false
})

const LoadBalancerStackProd = new LoadBalancerStack(app, 'LoadBalancerStack-prod', {
  env: {
    account: prodStackProps.account,
    region: prodStackProps.region
  },
  environment: prodStackProps.environment,
  vpc: VpcStackProd.vpc
})

const LambdaStackProd = new LambdaStack(app, 'LambdaStack-prod', {
  env: {
    account: prodStackProps.account,
    region: prodStackProps.region,
  },
  environment: prodStackProps.environment,
  ckanInstance: DatabaseStackProd.ckanInstance,
  ckanAdminCredentials: DatabaseStackProd.ckanAdminCredentials,
  vpc: VpcStackProd.vpc,
})

const CertificateStackProd = new CertificateStack(app, 'CertificateStack-prod', {
  env: {
    account: prodStackProps.account,
    region: prodStackProps.region,
  },
  zone: DomainStackProd.publicZone,
  newZone: DomainStackProd.newPublicZone
})


const EcsClusterStackProd = new EcsClusterStack(app, 'EcsClusterStack-prod', {
  env: {
    account: prodStackProps.account,
    region: prodStackProps.region,
  },
  environment: prodStackProps.environment,
  vpc: VpcStackProd.vpc
})

const FileSystemStackProd = new FileSystemStack(app, 'FilesystemStack-prod', {
  env: {
    account: prodStackProps.account,
    region: prodStackProps.region,
  },
  environment: prodStackProps.environment,
  vpc: VpcStackProd.vpc,
  terminationProtection: true
})


const RestricteddataParameterStackProd = new RestricteddataParameterStack(app, 'RestricteddataParameterStack-prod', {
  env: {
    account: prodStackProps.account,
    region: prodStackProps.region,
  },
  environment: prodStackProps.environment,
})

const NginxStackProd = new NginxStack(app, 'NginxStack-prod', {
  env: {
    account: prodStackProps.account,
    region: prodStackProps.region,
  },
  envProps: envProps,
  environment: prodStackProps.environment,
  vpc: VpcStackProd.vpc,
  allowRobots: "false",
  certificate: CertificateStackProd.certificate,
  newCertificate: CertificateStackProd.newCertificate,
  cluster: EcsClusterStackProd.cluster,
  namespace: EcsClusterStackProd.namespace,
  domainName: prodStackProps.domainName,
  fqdn: prodStackProps.fqdn,
  secondaryDomainName: prodStackProps.secondaryDomainName,
  secondaryFqdn: prodStackProps.secondaryFqdn,
  loadBalancer: LoadBalancerStackProd.loadBalancer,
  zone: DomainStackProd.publicZone,
  newZone: DomainStackProd.newPublicZone,
  taskDef: {
    taskCpu: 256,
    taskMem: 512,
    taskMinCapacity: 1,
    taskMaxCapacity: 1
  },
  authSourceAddressesParameterName: RestricteddataParameterStackProd.authSourceAddressesParameterName
})

const SolrStackProd = new SolrStack(app, 'SolrStack-prod', {
  env: {
    account: prodStackProps.account,
    region: prodStackProps.region,
  },
  envProps: envProps,
  environment: prodStackProps.environment,
  cluster: EcsClusterStackProd.cluster,
  namespace: EcsClusterStackProd.namespace,
  taskDef: {
    taskCpu: 256,
    taskMem: 1024,
    taskMinCapacity: 1,
    taskMaxCapacity: 1
  },
  vpc: VpcStackProd.vpc,
  fileSystem: FileSystemStackProd.solrFs
})

const CkanStackProd = new CkanStack(app, 'CkanStack-prod', {
  env: {
    account: prodStackProps.account,
    region: prodStackProps.region,
  },
  envProps: envProps,
  environment: prodStackProps.environment,
  ckanInstance: DatabaseStackProd.ckanInstance,
  ckanInstanceCredentials: LambdaStackProd.ckanCredentials,
  ckanSysAdminSecret: DatabaseStackProd.ckanSysAdminSecret,
  cluster: EcsClusterStackProd.cluster,
  databaseSecurityGroup: DatabaseStackProd.databaseSecurityGroup,
  domainName: prodStackProps.domainName,
  namespace: EcsClusterStackProd.namespace,
  redisCluster: DatabaseStackProd.redisCluster,
  redisSecurityGroup: DatabaseStackProd.redisSecurityGroup,
  solrService: SolrStackProd.solrService,
  nginxService: NginxStackProd.nginxService,
  secondaryDomainName: prodStackProps.secondaryDomainName,
  fileSystem: FileSystemStackProd.ckanFs,
  taskDef: {
    taskCpu: 1024,
    taskMem: 2048,
    taskMinCapacity: 3,
    taskMaxCapacity: 3
  },
  cronTaskDef: {
    taskCpu: 256,
    taskMem: 1024,
    taskMinCapacity: 1,
    taskMaxCapacity: 1
  },
  vpc: VpcStackProd.vpc,
  analyticsEnabled: true,
  matomoSiteId: 48,
  matomoDomain: "suomi.matomo.cloud",
  matomoScriptDomain: "//cdn.matomo.cloud/suomi.matomo.cloud/",
  sentryTracesSampleRate: "0.1",
  sentryProfilesSampleRate: "0.1"
})


const ShieldParameterStackProd = new ShieldParameterStack(app, 'ShieldParameterStack-prod', {
  env: {
    account: prodStackProps.account,
    region: prodStackProps.region,
  },
  environment: prodStackProps.environment,
})

const ShieldStackProd = new ShieldStack(app, 'ShieldStack-prod', {
  env: {
    account: prodStackProps.account,
    region: prodStackProps.region,
  },
  environment: prodStackProps.environment,
  loadBalancer: LoadBalancerStackProd.loadBalancer,
  rateLimitRequestSamplingEnabled: false,
  highPriorityRequestSamplingEnabled: false,
  bannedIpsRequestSamplingEnabled: false,
  requestSampleAllTrafficEnabled: false,
  bannedIpListParameterName: ShieldParameterStackProd.bannedIpListParameterName,
  whitelistedIpListParameterName: ShieldParameterStackProd.whitelistedIpListParameterName,
  highPriorityCountryCodeListParameterName: ShieldParameterStackProd.highPriorityCountryCodeListParameterName,
  highPriorityRateLimitParameterName: ShieldParameterStackProd.highPriorityRateLimitParameterName,
  rateLimitParameterName: ShieldParameterStackProd.rateLimitParameterName,
  managedRulesParameterName: ShieldParameterStackProd.managedRulesParameterName,
  snsTopicArnParameterName: ShieldParameterStackProd.snsTopicArnParameterName,
  wafAutomationArnParameterName: ShieldParameterStackProd.wafAutomationArnParameterName,
  evaluationPeriodParameterName: ShieldParameterStackProd.evaluationPeriodParameterName
})

const MonitoringStackProd = new MonitoringStack(app, 'MonitoringStack-prod', {
  sendToZulipLambda: LambdaStackProd.sendToZulipLambda,
  env: {
    account: prodStackProps.account,
    region: prodStackProps.region,
  }
});
