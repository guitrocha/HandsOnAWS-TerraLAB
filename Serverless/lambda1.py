import json
import ssl
import time

import boto3
import requests
import stomp


def main(event, context):
    try:
        print("Getting query params")
        pokemon = event["queryStringParameters"]["pokemon"]

        print(f"Requesting {pokemon} to PokeAPI.")
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}")
        responseDict = json.loads(response.text)
        print(f"Name = {responseDict['name']}, Types = {responseDict['types']}")

        print("Connecting to Secrets Manager.")
        client = boto3.client("secretsmanager")
        secret_name = "tutorial/mq/users"
        try:
            print("Getting secrets values")
            secret_value = client.get_secret_value(SecretId=secret_name)
        except Exception as e:
            raise e
        else:
            secretDict = json.loads(secret_value["SecretString"])
            username = secretDict["username"]
            password = secretDict["password"]

            print("Connecting to MQ.")
            client = boto3.client("mq")
            print("Getting broker IP")
            brokerInfo = client.describe_broker(BrokerId="fila-pokemon")
            ipport = (brokerInfo["BrokerInstances"][0]["IpAddress"], "61614")
            print(f"ip/port = {ipport}")

            conn = stomp.Connection([ipport])
            conn.set_ssl(for_hosts=[ipport], ssl_version=ssl.PROTOCOL_TLS)
            conn.connect(username, password, wait=True)
            conn.send(
                body=json.dumps(responseDict),
                destination="save-pokemon",
            )
            time.sleep(0.8)
            print("Function is over.")

        body = {
            "message": f"Pokémon {responseDict['name']} sent to queue",
            "input": event,
        }
        response = {"statusCode": 200, "body": json.dumps(body)}
        print(f"Lambda return = {body}")
    except Exception as error:
        body = {
            "message": f"Error: {error}",
            "input": event,
        }
        response = {"statusCode": 400, "body": json.dumps(body)}
        print(f"Lambda return = {body}")
    return response
