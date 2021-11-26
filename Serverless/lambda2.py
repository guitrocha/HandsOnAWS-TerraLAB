import base64
import json

import boto3


def main(event, context):
    try:
        print("Getting consumed message.")
        message = event["messages"][0]["data"]

        print("Decoding message.")
        message = base64.b64decode(message).decode("utf-8")

        print("Converting to dictionary (like a json)")
        pokemon = json.loads(message)

        temp = f"/tmp/{pokemon['name']}.json"
        file = open(temp, "w")
        json.dump(pokemon, file, indent=4)
        file.close()

        print("Connecting to s3.")
        client = boto3.client("s3")
        print(
            f"Sending {pokemon['name']} json to s3 partition {pokemon['types'][0]['type']['name']}"
        )
        client.upload_file(
            temp,
            "bucket-pokemon-tutorial-v2",
            f"{pokemon['types'][0]['type']['name']}/{pokemon['name']}.json",
        )
        print("Function is over.")

        body = {
            "message": f"Pokémon {pokemon['name']} sent to s3 partition {pokemon['types'][0]['type']['name']}",
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
