import { Handler } from "aws-lambda";

import {GetSecretValueCommand, SecretsManagerClient} from "@aws-sdk/client-secrets-manager";

import { knex } from 'knex';


const {
  CKAN_SECRET,
  ADMIN_SECRET } = process.env

export const handler: Handler = async (event, context) => {

  const secretsManagerClient = new SecretsManagerClient({region: "eu-west-1"})
  const command = new GetSecretValueCommand({
    SecretId: ADMIN_SECRET
  })
  const response = await secretsManagerClient.send(command);

  const credentials = response.SecretString

  const ckanCommand = new GetSecretValueCommand({
    SecretId: CKAN_SECRET
  })

  const ckanResponse = await secretsManagerClient.send(ckanCommand);
  const ckanCredentials = ckanResponse.SecretString

  if (credentials === undefined || ckanCredentials === undefined) {
    console.error('Configured credentials not found in secrets.')
    return {
      statusCode: 500,
      body: 'Configured credentials not found in secrets.'
    }
  }
  
  const credObj = JSON.parse(credentials)
  const ckanCredentialObj = JSON.parse(ckanCredentials)

  const client = knex({
    client: 'pg',
    connection: {
      user: credObj.username,
      password: credObj.password,
      host: credObj.host,
      port: credObj.port,
      database: "postgres"
    }
  })

  try {
    let ckanUser = ckanCredentialObj.username;
    let password = ckanCredentialObj.password;
    await client.raw(
      "SET LOCAL log_statement = 'none';" +
      `CREATE ROLE ${ckanUser} LOGIN PASSWORD '${password}'; `);
    console.log("Created ckan user account")
  } catch (err) {
    if (err && typeof err === 'object') {
      console.log(err.toString().replace(/PASSWORD\s(.*;)/, "***"))
    }
  }

  try {
    await client.raw("GRANT :ckanUser: TO :admin:; ", {
      ckanUser: ckanCredentialObj.username,
      admin: credObj.username
    })
    console.log("Granted 'ckan' role to admin")
  }
  catch (err) {
    if (err && typeof err === 'object') {
      console.log(err.toString().replace(/PASSWORD\s(.*;)/, "***"))
    }
  }


  try {
    await client.raw("CREATE DATABASE :ckanDb: OWNER :ckanUser: ENCODING 'utf-8'; ",
      {
        ckanDb: "ckan",
        ckanUser: ckanCredentialObj.username
      });
    console.log("Created database ckan")
  } catch (err) {
    if (err && typeof err === 'object') {
      console.log(err.toString().replace(/PASSWORD\s(.*;)/, "***"))
    }
  }

  return {
    statusCode: 200,
    body: "Db and users created"
  }
}
