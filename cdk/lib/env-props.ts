import {Stack} from "aws-cdk-lib";

export interface EnvProps {
  REGISTRY: string;
  REPOSITORY: string;
  NGINX_IMAGE_TAG: string;
  SOLR_IMAGE_TAG: string;
  CKAN_IMAGE_TAG: string;
}

export function getRepositoryArn(stack: Stack, registryURI: string, repository: string) {

  const parsedRepository = registryURI.match(/(\d{12})\.dkr\.ecr.(.*)\.amazonaws\.com/)

  if (parsedRepository) {
    const account = parsedRepository[0]
    const region = parsedRepository[1]
    return Stack.of(stack).formatArn({
      account: account,
      region: region,
      resource: "repository",
      service: "ecr",
      resourceName: repository
    })
  }

  return ""
}
