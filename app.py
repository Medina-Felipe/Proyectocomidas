import os
import requests
import csv
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("SPOONACULAR_KEY")

def obtener_nutricion(ingredientes):
    url = "https://api.spoonacular.com/recipes/guessNutrition"
    params_base = {
        "apiKey": API_KEY
    }
    resultados = []
    for texto in ingredientes:
        params = params_base.copy()
        params["title"] = texto
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if all(k in data for k in ["calories", "fat", "carbs", "protein"]):
                resultados.append({
                    "name": texto,
                    "calories": data["calories"].get("value", 0),
                    "fat": data["fat"].get("value", 0),
                    "carbs": data["carbs"].get("value", 0),
                    "protein": data["protein"].get("value", 0)
                })
            else:
                print(f"[Advertencia] Datos incompletos para: {texto}")
                print("Respuesta:", data)
        else:
            print(f"[Error] {response.status_code} - {response.text}")
    return resultados

def guardar_csv(datos, archivo):
    with open(archivo, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "calories", "fat", "carbs", "protein"])
        for item in datos:
            writer.writerow([
                item["name"],
                item["calories"],
                item["fat"],
                item["carbs"],
                item["protein"]
            ])

if __name__ == "__main__":
    ingredientes = [
    "1 cup cooked white rice", "100g grilled chicken breast", "1 tablespoon olive oil", "1 medium boiled egg",
    "1 slice whole wheat bread", "1 banana", "1 apple", "1 cup steamed broccoli", "1 cup skim milk",
    "1 tablespoon peanut butter", "1 cup cooked oatmeal", "1 slice cheddar cheese", "1 cup orange juice",
    "1 cup chopped lettuce", "1/2 cup cooked quinoa", "1 cup strawberries", "1 cup blueberries",
    "1 cup low-fat yogurt", "1 baked sweet potato", "1 grilled salmon fillet", "1 boiled potato",
    "1/2 avocado", "1 medium carrot", "1 medium cucumber", "1/2 cup canned tuna", "1 tablespoon honey",
    "1 cup vegetable soup", "1 turkey sandwich", "1 hard boiled egg", "1 tablespoon mayonnaise",
    "1 tablespoon ketchup", "1 slice ham", "1 small grilled steak", "1 small corn tortilla",
    "1 slice mozzarella cheese", "1 slice pineapple", "1 cup grapes", "1 tablespoon chia seeds",
    "1/2 cup black beans", "1/2 cup lentils", "1 small pear", "1 cup almond milk", "1 tablespoon butter",
    "1 tablespoon sunflower oil", "1 tablespoon flaxseed", "1 small croissant", "1 chocolate chip cookie",
    "1 small slice of cake", "1 cup cereal", "1/2 cup mixed nuts", "1 small hamburger patty",
    "1/2 cup cooked spinach", "1/2 cup green peas", "1 hard boiled egg white", "1 slice salami",
    "1 cup watermelon cubes", "1 cup mango chunks", "1 tablespoon soy sauce", "1 tablespoon barbecue sauce",
    "1/2 cup mashed potatoes", "1/2 cup coleslaw", "1 slice turkey breast", "1 cup kale", "1 cup cooked pasta",
    "1 tablespoon maple syrup", "1 slice bacon", "1/2 cup cooked brown rice", "1 cup cucumber slices",
    "1 cup mixed salad", "1 tablespoon hummus", "1 tablespoon cream cheese", "1 glass red wine",
    "1 can soda", "1 medium chocolate bar", "1 small avocado toast", "1 fried egg", "1 boiled corn cob",
    "1 small portion of lasagna", "1 slice pepperoni pizza", "1 cup tomato soup", "1 grilled chicken thigh",
    "1 chicken nugget", "1 tablespoon pesto sauce", "1 croissant with jam", "1 slice raisin bread",
    "1 granola bar", "1 bowl miso soup", "1/2 cup edamame", "1 cup sautéed mushrooms", "1 tablespoon tahini",
    "1 soft boiled egg", "1 tablespoon ranch dressing", "1 slice Swiss cheese", "1 bowl ramen noodles",
    "1 sushi roll", "1 piece sashimi salmon", "1 cup zucchini noodles", "1 veggie burger patty",
    "1 protein shake", "1 energy drink", "1 hard candy", "1 cup iced tea", "1 tablespoon tomato paste"
]

    datos = obtener_nutricion(ingredientes)
    guardar_csv(datos, "/muestra_recetas.csv")