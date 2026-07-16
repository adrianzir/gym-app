#paso 1 import el modulo requests
import requests 

#paso 2 declarar una variable con la ruta o link de la api
base_url = "https://pokeapi.co/api/v2/"

#paso 3 función que traerá los datos de la app
def get_pokemon_info(name) :
    url = f"{base_url}/pokemon/{name}"
    response = requests.get(url)
    
    if response.status_code == 200:
        pokemon_data = response.json()
        return pokemon_data
    else:
        print(f"failed to retrieve data {response.status_code}")

#paso 4 declaramos variable que contiene el parametro con el que probaremos la función
pokemon_name = "gyarados"

#paso 5 declaramos variable que almacena lo que traerá nuestra función
pokemon_info = get_pokemon_info(pokemon_name)

#paso 6 hacemos un IF para pintar en la consola los datos que nos trajo la función y guardamos en la variable anterior
if pokemon_info:
    print(f"name: {pokemon_info["name"]}")
    print(f"id: {pokemon_info["id"]}")
    print(f"height: {pokemon_info["height"]}")
    print(f"weight: {pokemon_info["weight"]}")