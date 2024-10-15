import {aws_backup, aws_ec2} from "aws-cdk-lib";
import {NetworkStackProps} from "./network-stack-props";

export interface DatabaseStackProps extends NetworkStackProps {
    multiAz: boolean;
    backups: boolean;
    backupPlan: aws_backup.BackupPlan;
    cacheNodeType: string;
    numCacheNodes: number;
    terminationProtection: boolean;
    restoreFromSnapshot: boolean;
    snapshotIdentifier?: string;
}

