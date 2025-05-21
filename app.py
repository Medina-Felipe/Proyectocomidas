import requests
import csv
import os
from time import sleep

API_KEY = "41e5f34cb39049149b611ae999d744c9"
OUTPUT_FILE = "data/recetas.csv"

# Campo adicional: nombre de la receta
campo_nombre = "title"

variables_numericas = [
    "servings",
    "readyInMinutes",
    "cookingMinutes",
    "preparationMinutes",
    "healthScore",
    "spoonacularScore",
    "pricePerServing"
]

variables_categoricas = [
    "cheap",
    "dairyFree",
    "glutenFree",
    "sustainable",
    "vegan",
    "vegetarian",
    "veryHealthy",
    "veryPopular"
]

def obtener_recetas(n=100):
    recetas = []
    offset = 0
    while len(recetas) < n:
        url = f"https://api.spoonacular.com/recipes/complexSearch"
        params = {
            "apiKey": API_KEY,
            "number": 10,
            "offset": offset,
            "addRecipeInformation": True
        }
        try:
            r = requests.get(url, params=params)
            r.raise_for_status()
            data = r.json()

            for receta in data.get("results", []):
                receta_filtrada = {}
                try:
                    receta_filtrada[campo_nombre] = receta[campo_nombre]
                    for campo in variables_numericas + variables_categoricas:
                        receta_filtrada[campo] = receta[campo]
                    recetas.append(receta_filtrada)
                    if len(recetas) >= n:
                        break
                except KeyError:
                    continue  # Saltar si falta alguna variable

            offset += 10
            sleep(1)  # evitar rate limit
        except Exception as e:
            print("Error:", e)
            break
    return recetas

def guardar_csv(recetas, archivo):
    os.makedirs(os.path.dirname(archivo), exist_ok=True)
    columnas = [campo_nombre] + variables_numericas + variables_categoricas

    with open(archivo, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=columnas)
        writer.writeheader()
        for receta in recetas:
            writer.writerow(receta)

if __name__ == "__main__":
    print("Extrayendo recetas...")
    recetas = obtener_recetas(100)
    print(f"Recetas extraídas: {len(recetas)}")
    guardar_csv(recetas, OUTPUT_FILE)
    print(f"Datos guardados en {OUTPUT_FILE}")
