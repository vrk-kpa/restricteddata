#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { DomainStack } from '../lib/domain-stack';
import {VpcStack} from "../lib/vpc-stack";
import {DatabaseStack} from "../lib/database-stack";
import {KmsKeyStack} from "../lib/kms-key-stack";
import {LoadBalancerStack} from "../lib/load-balancer-stack";

const app = new cdk.App();

const prodStackProps = {
    account: '157248445006',
    region: 'eu-north-1'
}

const devStackProps = {
    account: '332833619545',
    region: 'eu-north-1'
}

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
    }
})

const DatabaseStackDev = new DatabaseStack(app, 'DatabaseStack-dev', {
    env: {
        account: devStackProps.account,
        region: devStackProps.region
    },
    environment: "dev",
    vpc: VpcStackDev.vpc,
    multiAz: false,
    databaseEncryptionKey: KmsKeyStackDev.databaseEncryptionKey
})

const LoadBalancerStackDev = new LoadBalancerStack(app, 'LoadBalancerStack-dev', {
    env: {
        account: devStackProps.account,
        region: devStackProps.region
    },
    environment: "dev",
    vpc: VpcStackDev.vpc
})



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
    }
})

const DatabaseStackProd = new DatabaseStack(app, 'DatabaseStack-prod', {
    env: {
        account: prodStackProps.account,
        region: prodStackProps.region
    },
    environment: "prod",
    vpc: VpcStackProd.vpc,
    multiAz: false,
    databaseEncryptionKey: KmsKeyStackProd.databaseEncryptionKey,

})



const DomainStackProd = new DomainStack(app, 'DomainStack-prod', {
    env: {
        account: prodStackProps.account,
        region: prodStackProps.region
    },

});
