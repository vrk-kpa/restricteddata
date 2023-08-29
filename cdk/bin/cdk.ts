#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { DomainStack } from '../lib/domain-stack';
import {VpcStack} from "../lib/vpc-stack";

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

const VpcStackProd = new VpcStack(app, 'VpcStack-prod', {
    env: {
        account: prodStackProps.account,
        region: prodStackProps.region
    }
})

const DomainStackProd = new DomainStack(app, 'DomainStack-prod', {
    env: {
        account: prodStackProps.account,
        region: prodStackProps.region
    },

});