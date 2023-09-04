import {aws_ec2, aws_rds, Stack} from "aws-cdk-lib";
import {Construct} from "constructs";
import * as ssm from 'aws-cdk-lib/aws-ssm';
import {DatabaseStackProps} from "./database-stack-props";
import {Credentials} from "aws-cdk-lib/aws-rds";
import {InstanceType, SubnetType} from "aws-cdk-lib/aws-ec2";

export class DatabaseStack extends Stack {
    constructor(scope: Construct, id: string, props: DatabaseStackProps) {
        super(scope, id, props);


        const pDatabaseInstanceType = ssm.StringParameter.fromStringParameterName(this, 'pDatabaseInstanceType',
            `/${props.environment}/cdk/database_instance_type`)



        const databaseSecurityGroup = new aws_ec2.SecurityGroup(this, 'databaseSecurityGroup', {
            vpc: props.vpc
        })

        const databaseSecret = new aws_rds.DatabaseSecret(this,'databaseAdminSecret', {
            username: "databaseAdmin",
            encryptionKey: props.databaseEncryptionKey
        });

        const databaseCredentials = Credentials.fromSecret(databaseSecret);


        const databaseInstance = new aws_rds.DatabaseInstance(this, 'databaseInstance', {
            engine: aws_rds.DatabaseInstanceEngine.POSTGRES,
            credentials: databaseCredentials,
            vpc: props.vpc,
            port: 5432,
            instanceType: new InstanceType(pDatabaseInstanceType.stringValue),
            multiAz: props.multiAz,
            allocatedStorage: 20,
            maxAllocatedStorage: 100,
            vpcSubnets: {
                subnets: props.vpc.privateSubnets
            },
            securityGroups: [
                databaseSecurityGroup
            ]

        })

    }
}
