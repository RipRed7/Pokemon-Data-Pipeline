#connect to api
import requests

base_url = "https://pokeapi.co/api/v2/"

def getPokemonInfo(name):
    url = f"{base_url}/pokemon/{name}"
    response = requests.get(url)

    if response.status_code == 200:
        pokemonData = response.json()
        return pokemonData
    else:
        print(f"Failed to retrieve data {response.status_code}")


pokemoneName = "torterra"
pokemonInfo = getPokemonInfo(pokemoneName)

if pokemonInfo:
    print(f"Name: {pokemonInfo["name"]}")
    print(f"ID: {pokemonInfo["id"]}")
    print(f"Height: {pokemonInfo["height"]}")
    print(f"Weight: {pokemonInfo["weight"]}")
    