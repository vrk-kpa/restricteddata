#!/usr/bin/env node
import 'source-map-support/register';
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

const app = new cdk.App();

const prodStackProps = {
    account: '157248445006',
    region: 'eu-north-1'
}

const devStackProps = {
    account: '332833619545',
    region: 'eu-north-1'
}

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
    environment: "dev",
    vpc: VpcStackDev.vpc,
})

const BackupStackDev = new BackupStack(app, 'BackupStack-dev', {
    env: {
        account: devStackProps.account,
        region: devStackProps.region,
    },
    vpc: VpcStackDev.vpc,
    environment: "dev",
    importVault: false,
    backups: true
})

const DatabaseStackDev = new DatabaseStack(app, 'DatabaseStack-dev', {
    env: {
        account: devStackProps.account,
        region: devStackProps.region
    },
    environment: "dev",
    vpc: VpcStackDev.vpc,
    multiAz: false,
    backups: true,
    backupPlan: BackupStackDev.backupPlan
})

const LoadBalancerStackDev = new LoadBalancerStack(app, 'LoadBalancerStack-dev', {
    env: {
        account: devStackProps.account,
        region: devStackProps.region
    },
    environment: "dev",
    vpc: VpcStackDev.vpc
})

const LambdaStackDev = new LambdaStack(app, 'LambdaStack-dev', {
  env: {
    account: devStackProps.account,
    region: devStackProps.region,
  },
  environment: "dev",
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
    loadBalancer: LoadBalancerStackDev.loadBalancer,
    subDomainName: "dev"
})

const CertificateStackDev = new CertificateStack(app, 'CertificateStack-dev', {
    env: {
        account: devStackProps.account,
        region: devStackProps.region,
    },
    zone: SubDomainStackDev.subZone
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
    environment: "prod",
    vpc: VpcStackProd.vpc,
})

const BackupStackProd = new BackupStack(app, 'BackupStack-prod', {
    env: {
        account: prodStackProps.account,
        region: prodStackProps.region,
    },
    vpc: VpcStackProd.vpc,
    environment: "prod",
    importVault: false,
    backups: true
})

const DatabaseStackProd = new DatabaseStack(app, 'DatabaseStack-prod', {
    env: {
        account: prodStackProps.account,
        region: prodStackProps.region
    },
    environment: "prod",
    vpc: VpcStackProd.vpc,
    multiAz: false,
    backups: true,
    backupPlan: BackupStackProd.backupPlan

})

const LoadBalancerStackProd = new LoadBalancerStack(app, 'LoadBalancerStack-prod', {
    env: {
        account: prodStackProps.account,
        region: prodStackProps.region
    },
    environment: "prod",
    vpc: VpcStackProd.vpc
})

const LambdaStackProd = new LambdaStack(app, 'LambdaStack-prod', {
  env: {
    account: prodStackProps.account,
    region: prodStackProps.region,
  },
  environment: "prod",
  ckanInstance: DatabaseStackProd.ckanInstance,
  ckanAdminCredentials: DatabaseStackProd.ckanAdminCredentials,
  vpc: VpcStackProd.vpc,
})

const CertificateStackProd = new CertificateStack(app, 'CertificateStack-prod', {
  env: {
    account: devStackProps.account,
    region: devStackProps.region,
  },
  zone: DomainStackProd.publicZone
})