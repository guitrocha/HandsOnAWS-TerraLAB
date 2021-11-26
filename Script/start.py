import json

import requests


def call_lambda(pokemon: str):
    params = {"pokemon": pokemon}
    response = requests.get(
        "https://t6gv53ghih.execute-api.us-east-1.amazonaws.com/dev/lambda1/pokemon",
        params=params,
    )
    print(
        f'\n============\nSTATUS CODE: {response.status_code}\nREASON: {response.reason}\nRESPONSE: {json.loads(response.text)["message"]}\n'
    )


if __name__ == "__main__":
    with open("poke-names.txt", "r") as file:
        pokemons = [pokemon.rstrip("\n") for pokemon in file]
    print(pokemons)

    for pokemon in pokemons:
        call_lambda(pokemon)
