import {CommonStackProps} from "./common-stack-props";
import {aws_backup} from "aws-cdk-lib";

export interface DatabaseStackProps extends CommonStackProps {
    multiAz: boolean;
    backups: boolean;
    backupPlan: aws_backup.BackupPlan;
    cacheNodeType: string;
    numCacheNodes: number;
    terminationProtection: boolean;
}

