import {Stack} from "aws-cdk-lib";

export interface EnvProps {
  REGISTRY: string;
  REPOSITORY: string;
  NGINX_IMAGE_TAG: string;
  SOLR_IMAGE_TAG: string;
  CKAN_IMAGE_TAG: string;
}

export function getRepositoryArn(stack: Stack, registry: string, repository: string) {

  const parsedRegistry = registry.match(/(\d{12})\.dkr\.ecr.(.*)\.amazonaws\.com/)

  if (parsedRegistry === null) {
    throw new Error(`Invalid repository URI: ${registry} is not valid`)
  }

  const account = parsedRegistry[1]
  const region = parsedRegistry[2]
  return Stack.of(stack).formatArn({
    account: account,
    region: region,
    resource: "repository",
    service: "ecr",
    resourceName: repository
  })

}


export function parseEnv(key: string): string {
  let val = process.env[key];
  if (val == null) {
    throw new Error(`parseEnv error: ${key} is undefined or null!`);
  }
  return val;
}
