export interface EcsTaskDefinitionProps {
  /**
   * The number of cpu units used by the task.
   * 256 (0.25 vCPU), 512 (0.5 vCPU), 1024 (1.0 vCPU), 2048 (2.0 vCPU), 4096 (4.0 vCPU)
   */
  taskCpu: number;
  /**
   * The amount (in MiB) of memory used by the task.
   * 0.25 vCPU: 512MB, 1024MB, 2048MB
   * 0.5  vCPU: 1024MB, 2048MB, 3072MB, 4096MB
   * 1.0  vCPU: 2048MB, 3072MB, 4096MB, 5120MB, 6144MB, 7168MB, 8192MB
   * 2.0  vCPU: 4096MB, 16384MB in increments of 1024MB
   * 4.0  vCPU: 8192MB, 30720MB in increments of 1024MB
   */
  taskMem: number;
  /**
   * Minimum number of tasks at a time.
   */
  taskMinCapacity: number;
  /**
   * Maximum number of tasks at a time.
   */
  taskMaxCapacity: number;
  /**
   * The amount (in GiB) of ephemeral storage to be allocated to the task.
   */
  taskStorage?: number;
}
