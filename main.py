from dotenv import load_dotenv
import requests
import json
import snowflake.connector
import os

#choose pokemon to gather data about
POKEMON = "pikachu"

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
pokemonName = POKEMON

#Data of pokemon
pokemonInfo = getPokemonInfo(pokemonName)
pokeBaseXP = pokemonInfo['base_experience']
pokeName = pokemonInfo['name']
pokeHeight = pokemonInfo['height']
pokeWeight = pokemonInfo['weight']

#copy data set to file for safety  
with open("pokemonDataCopy.json", "w") as json_file:
    json.dump(pokemonInfo, json_file)

#Store data in JSON file
with open("pokemonData.json", "w") as json_file:
    json.dump(pokemonInfo, json_file, indent=4, sort_keys=True)


cursor = conn.cursor()

#create table if one does not exist
cursor.execute("""
        CREATE OR REPLACE TABLE Pokemon_Info (
            Name STRING,
            BaseXP INT,
            Height INT,
            Weight INT
        );
    """)


try:
    #insertion into table
    cursor.execute(
        "INSERT INTO Pokemon_Info (Name, BaseXP, Height, Weight) VALUES (%s, %s, %s, %s)",
        (pokeName, pokeBaseXP, pokeHeight, pokeWeight)   
    )

    conn.commit()

    #print table to validate data insertion
    cursor.execute("SELECT * FROM Pokemon_Info;")
    for entry in cursor:
        print(entry)
    
    #success message :D
    print("Data inserted successfully.")

except Exception as e:
    #Error Message :(
    print(f"An error occurred: {e}")
finally:
    #close connection
    conn.commit()
    cursor.close()
    conn.close()
