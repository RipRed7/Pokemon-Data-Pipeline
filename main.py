from dotenv import load_dotenv
import requests
import json
import snowflake.connector
import os

load_dotenv()

user = os.getenv('SNOWFLAKE_USER')
password = os.getenv('SNOWFLAKE_PASSWORD')

#connect to snowflake account
conn = snowflake.connector.connect(
    user = user,
    password= password,
    account='AUALWTU-QJ46454',
    warehouse='COMPUTE_WH',
    database='POKEMON_DATA',
    schema='PUBLIC'
)

cursor = conn.cursor()

create_table_query = """
CREATE OR REPLACE TABLE Pokemon_Info (
    column1 STRING,
    column2 INT,
    column3 DATE
)
"""

cursor.execute(create_table_query)

#base url of website im pulling data from
base_url = "https://pokeapi.co/api/v2/"

#method to request response of data from API
def getPokemonInfo(name):
    #url of specific pokemon
    url = f"{base_url}/pokemon/{name}"

    #requests response
    response = requests.get(url)

    #checks connection, if connection is good store JSON data and return it
    if response.status_code == 200:
        pokemonData = response.json()
        return pokemonData
    #Error Message
    else:
        print(f"Failed to retrieve data {response.status_code}")


#name of pokemon to request data for
pokemoneName = "torterra"

#Data of pokemon
pokemonInfo = getPokemonInfo(pokemoneName)
df = pokemonInfo

#copy data set to file for safety  
with open("pokemonDataCopy.json", "w") as json_file:
    json.dump(pokemonInfo, json_file, indent=4)

#Store data in JSON file
with open("pokemonData.json", "w") as json_file:
    json.dump(pokemonInfo, json_file, indent=4, sort_keys=True)
