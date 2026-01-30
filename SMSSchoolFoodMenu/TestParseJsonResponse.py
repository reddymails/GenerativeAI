import requests
from datetime import datetime

BASE_URL = "https://pausd.api.nutrislice.com/menu/api/weeks/school"
SCHOOL = "juana-briones-es"

MEALS = ["breakfast", "lunch"]   # snack removed (not supported)

def build_url(meal, date_obj):
    y = date_obj.strftime("%Y")
    m = date_obj.strftime("%m")
    d = date_obj.strftime("%d")
    return f"{BASE_URL}/{SCHOOL}/menu-type/{meal}/{y}/{m}/{d}?format=json"

def fetch_menu_for_meal(meal, date_obj):
    url = build_url(meal, date_obj)

    resp = requests.get(url, timeout=10)

    if resp.status_code == 404:
        return []   # meal not offered

    resp.raise_for_status()
    data = resp.json()

    days = data.get("days") or []   # prevents NoneType error
    today_str = date_obj.strftime("%Y-%m-%d")

    items = []

    for day in days:
        if day.get("date") == today_str:
            for item in day.get("menu_items") or []:
                food = item.get("food") or {}
                name = food.get("name")
                if name:
                    items.append(name)
            break

    return items

def get_all_meals():
    today = datetime.now()
    results = {}

    for meal in MEALS:
        try:
            results[meal] = fetch_menu_for_meal(meal, today)
        except Exception as e:
            results[meal] = [f"Error: {e}"]

    return results

def pretty_print(menus):
    for meal, items in menus.items():
        print(f"\n{meal.upper()}:")
        if items:
            for i in items:
                print(f" - {i}")
        else:
            print(" No menu available")

# -------------------------
# Run
# -------------------------
if __name__ == "__main__":
    menus = get_all_meals()
    pretty_print(menus)
