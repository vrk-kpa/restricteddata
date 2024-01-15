import {Stack} from "aws-cdk-lib";
import {Construct} from "constructs";

import * as bak from "aws-cdk-lib/aws-backup";
import {BackupStackProps} from "./backup-stack-props";

export class BackupStack extends Stack {
  readonly backupPlan: bak.BackupPlan

  constructor(scope: Construct, id: string, props: BackupStackProps) {
    super(scope, id, props);

    if (props.backups) {

      let backupVault = null;
      let backupVaultName = `restricteddata-vault-${props.environment}`;
      let backupPlanName = `restricteddata-plan-${props.environment}`;

      if (props.importVault) {
        backupVault = bak.BackupVault.fromBackupVaultName(this, 'backupVault', backupVaultName)
      } else {
        backupVault = new bak.BackupVault(this, 'backupVault', {
          backupVaultName: backupVaultName,
        });
      }

      this.backupPlan = new bak.BackupPlan(this, 'backupPlan', {
        backupPlanName: backupPlanName,
        backupVault: backupVault,
        backupPlanRules: [
          bak.BackupPlanRule.daily(),
          bak.BackupPlanRule.weekly(),
          bak.BackupPlanRule.monthly1Year()
        ],
      });
    }
  }
}
