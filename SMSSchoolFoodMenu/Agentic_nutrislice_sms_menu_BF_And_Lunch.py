
######################################################################
# Sample code to check school website and get the JSO response to see
# what's up for Breakfast and Lunch.
# We can schedule this as a JOB to run daily at 7 AM . We can change the time.
#
# Twilio internally uses appier libray and to fix that i had to  uninstall and re install exact versions.
#  which python
# C:\msys64\mingw64\bin\python.exe
# C:\Users\rreddy\AppData\Local\Microsoft\WindowsApps\python.exe
# C:\Users\rreddy\AppData\Local\Programs\Python\Python314\python.exe
#
# "C:\Users\rreddy\AppData\Local\Programs\Python\Python314\python.exe" -m pip uninstall -y twilio appier
# "C:\Users\rreddy\AppData\Local\Programs\Python\Python314\python.exe" -m pip uninstall -y twilio appier
# "C:\Users\rreddy\AppData\Local\Programs\Python\Python314\python.exe" -m pip install appier==1.34.5
# "C:\Users\rreddy\AppData\Local\Programs\Python\Python314\python.exe" -m pip install twilio==8.13.0
#####################################################################
import os
import requests
from twilio.rest import Client
from datetime import datetime
from dotenv import load_dotenv
import schedule, time

# ----------------------------
# ENV SETUP
# ----------------------------
load_dotenv("C:/Rama/Learn/AI/.env")

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_PHONE")
TO_PHONE = os.getenv("TO_PHONE")

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Nutrislice
DISTRICT = os.getenv("DISTRICT")          # pausd
SCHOOL_NAME = os.getenv("SCHOOL_NAME")    # juana-briones-es
# Was reading from env file if missing was defaulting to breakfast.
#MEAL = os.getenv("MEAL", "breakfast")
MEALS = ["breakfast", "lunch"]

# ----------------------------
# API URL BUILDER
# ----------------------------
def build_api_url(meal, date):
    y = date.strftime("%Y")
    m = date.strftime("%m")
    d = date.strftime("%d")
    return (
        f"https://{DISTRICT}.api.nutrislice.com/"
        f"menu/api/weeks/school/{SCHOOL_NAME}/"
        f"menu-type/{meal}/{y}/{m}/{d}?format=json"
    )

# ----------------------------
# FETCH MENU
# ----------------------------
def fetch_json_menu(meal):
    url = build_api_url(meal, datetime.now())
    print(f"[Fetching] {meal}: {url}")

    resp = requests.get(url, timeout=10)

    if resp.status_code == 404:
        return None

    resp.raise_for_status()
    return resp.json()

# ----------------------------
# PARSE MENU
# ----------------------------
def parse_menu(json_data, meal):
    if not json_data:
        return []

    days = json_data.get("days") or []
    today_str = datetime.now().strftime("%Y-%m-%d")

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

# ----------------------------
# BUILD SMS TEXT
# ----------------------------
def build_sms_text(all_menus):
    today = datetime.now().strftime("%Y-%m-%d")
    lines = [f"School Menu ({today})", ""]

    for meal, items in all_menus.items():
        lines.append(meal.upper())
        if items:
            for i in items:
                lines.append(f"- {i}")
        else:
            lines.append("No menu available")
        lines.append("")

    return "\n".join(lines)

# ----------------------------
# SEND SMS
# ----------------------------
def send_sms(message):
    sms = client.messages.create(
        body=message,
        from_=TWILIO_PHONE,
        to=TO_PHONE
    )
    print(f"[SMS Sent] {sms.sid}")


# ----------------------------
# MAIN JOB
# ----------------------------
def job():
    all_menus = {}

    for meal in MEALS:
        json_data = fetch_json_menu(meal)
        items = parse_menu(json_data, meal)
        all_menus[meal] = items

    sms_text = build_sms_text(all_menus)
    print(sms_text)
    send_sms(sms_text)

# ----------------------------
# RUN
# ----------------------------
if __name__ == "__main__":
    job()

    schedule.every().day.at("07:00").do(job)

    while True:
        schedule.run_pending()
        time.sleep(60)
