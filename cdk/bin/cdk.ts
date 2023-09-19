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

const app = new cdk.App();

const prodStackProps = {
  account: '157248445006',
  region: 'eu-north-1',
  environment: "prod"
}

const devStackProps = {
  account: '332833619545',
  region: 'eu-north-1',
  environment: "dev",
  domainName: "dev.rekisteridata.fi",
  secondaryDomainName: "dev.suojattudata.suomi.fi",
  fqdn: "rekisteridata.fi",
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
  }
})



const KmsKeyStackDev = new KmsKeyStack(app, 'KmsKeyStack-dev', {
  env: {
    account: devStackProps.account,
    region: devStackProps.region
  },
  envProps: envProps,
  environment: devStackProps.environment,
  vpc: VpcStackDev.vpc,
})

const BackupStackDev = new BackupStack(app, 'BackupStack-dev', {
  env: {
    account: devStackProps.account,
    region: devStackProps.region,
  },
  envProps: envProps,
  vpc: VpcStackDev.vpc,
  environment: devStackProps.environment,
  importVault: false,
  backups: true
})

const DatabaseStackDev = new DatabaseStack(app, 'DatabaseStack-dev', {
  env: {
    account: devStackProps.account,
    region: devStackProps.region
  },
  envProps: envProps,
  environment: devStackProps.environment,
  vpc: VpcStackDev.vpc,
  multiAz: false,
  backups: true,
  backupPlan: BackupStackDev.backupPlan,
  cacheNodeType: 'cache.t3.micro',
  numCacheNodes: 1
})

const LoadBalancerStackDev = new LoadBalancerStack(app, 'LoadBalancerStack-dev', {
  env: {
    account: devStackProps.account,
    region: devStackProps.region
  },
  envProps: envProps,
  environment: devStackProps.environment,
  vpc: VpcStackDev.vpc
})

const LambdaStackDev = new LambdaStack(app, 'LambdaStack-dev', {
  env: {
    account: devStackProps.account,
    region: devStackProps.region,
  },
  envProps: envProps,
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
  zone: SubDomainStackDev.subZone
})

const EcsClusterStackDev = new EcsClusterStack(app, 'EcsClusterStack-dev', {
  env: {
    account: devStackProps.account,
    region: devStackProps.region,
  },
  envProps: envProps,
  environment: devStackProps.environment,
  vpc: VpcStackDev.vpc
})

const FileSystemStackDev = new FileSystemStack(app, 'FilesystemStack-dev', {
  env: {
    account: devStackProps.account,
    region: devStackProps.region,
  },
  envProps: envProps,
  environment: devStackProps.environment,
  vpc: VpcStackDev.vpc
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
  cluster: EcsClusterStackDev.cluster,
  namespace: EcsClusterStackDev.namespace,
  domainName: devStackProps.domainName,
  fqdn: devStackProps.fqdn,
  secondaryDomainName: devStackProps.secondaryDomainName,
  secondaryFqdn: devStackProps.secondaryFqdn,
  loadBalancer: LoadBalancerStackDev.loadBalancer,
  zone: SubDomainStackDev.subZone,
  taskDef: {
    taskCpu: 256,
    taskMem: 512,
    taskMinCapacity: 1,
    taskMaxCapacity: 1
  }

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
  cluster: EcsClusterStackDev.cluster,
  databaseSecurityGroup: DatabaseStackDev.databaseSecurityGroup,
  domainName: devStackProps.domainName,
  namespace: EcsClusterStackDev.namespace,
  redisCluster: DatabaseStackDev.redisCluster,
  redisSecurityGroup: DatabaseStackDev.redisSecurityGroup,
  solrService: SolrStackDev.solrService,
  secondaryDomainName: devStackProps.secondaryDomainName,
  taskDef: {
    taskCpu: 256,
    taskMem: 1024,
    taskMinCapacity: 1,
    taskMaxCapacity: 1
  },
  vpc: VpcStackDev.vpc

})


// Production


const VpcStackProd = new VpcStack(app, 'VpcStack-prod', {
  env: {
    account: prodStackProps.account,
    region: prodStackProps.region
  }
})

const KmsKeyStackProd = new KmsKeyStack(app, 'KmsKeyStack-prod', {
  env: {
    account: prodStackProps.account,
    region: prodStackProps.region
  },
  envProps: envProps,
  environment: prodStackProps.environment,
  vpc: VpcStackProd.vpc,
})

const BackupStackProd = new BackupStack(app, 'BackupStack-prod', {
  env: {
    account: prodStackProps.account,
    region: prodStackProps.region,
  },
  envProps: envProps,
  vpc: VpcStackProd.vpc,
  environment: prodStackProps.environment,
  importVault: false,
  backups: true
})

const DatabaseStackProd = new DatabaseStack(app, 'DatabaseStack-prod', {
  env: {
    account: prodStackProps.account,
    region: prodStackProps.region
  },
  envProps: envProps,
  environment: prodStackProps.environment,
  vpc: VpcStackProd.vpc,
  multiAz: false,
  backups: true,
  backupPlan: BackupStackProd.backupPlan,
  cacheNodeType: 'cache.t3.micro',
  numCacheNodes: 1
})

const LoadBalancerStackProd = new LoadBalancerStack(app, 'LoadBalancerStack-prod', {
  env: {
    account: prodStackProps.account,
    region: prodStackProps.region
  },
  envProps: envProps,
  environment: prodStackProps.environment,
  vpc: VpcStackProd.vpc
})

const LambdaStackProd = new LambdaStack(app, 'LambdaStack-prod', {
  env: {
    account: prodStackProps.account,
    region: prodStackProps.region,
  },
  envProps: envProps,
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
  zone: DomainStackProd.publicZone
})
