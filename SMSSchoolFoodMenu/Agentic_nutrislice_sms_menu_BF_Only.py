#####################################################################
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
load_dotenv("C:/Rama/Learn/AI/.env")

# Twilio config
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_PHONE")
TO_PHONE = os.getenv("TO_PHONE")
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Nutrislice config
DISTRICT = os.getenv("DISTRICT")  # e.g., "pausd"
SCHOOL_NAME = os.getenv("SCHOOL_NAME")  # e.g., "juana-briones-es"
MEAL = os.getenv("MEAL", "breakfast")



def build_api_url(date: datetime):
    y = date.strftime("%Y")
    m = date.strftime("%m")
    d = date.strftime("%d")
    return (
        f"https://{DISTRICT}.api.nutrislice.com/"
        f"menu/api/weeks/school/{SCHOOL_NAME}/"
        f"menu-type/{MEAL}/{y}/{m}/{d}?format=json"
    )


def fetch_json_menu():
    url = build_api_url(datetime.now())
    print(f"[Fetching JSON] {url}")
    resp = requests.get(url, timeout=10)
    if resp.status_code != 200:
        print(f"[Error] HTTP {resp.status_code}")
        return None
    return resp.json()


def parse_menu(json_data):
    if not json_data:
        return None

    # Nutrislice JSON typically contains an array of days
    days = json_data.get("days", [])
    today_str = datetime.now().strftime("%Y-%m-%d")
    daily_items = []

    for day in days:
        if day.get("date") == today_str:
            for item in day.get("menu_items", []):
                food = item.get("food")
                if food and food.get("name"):
                    daily_items.append(food["name"])
            break

    if not daily_items:
        return f"No {MEAL} menu found for {today_str}"

    msg = f"{MEAL.title()} Menu ({today_str}):\n" + "\n".join(daily_items)
    return msg


def send_sms(message):
    if not message:
        return
    sms = client.messages.create(
        body=message,
        from_=TWILIO_PHONE,
        to=TO_PHONE
    )
    print(f"[SMS Sent] {sms.sid}")


def job():
    json_data = fetch_json_menu()
    text = parse_menu(json_data)
    print(text)
    send_sms(text)


if __name__ == "__main__":
    # run once now
    job()

    # schedule daily at 7am
    schedule.every().day.at("07:00").do(job)
    while True:
        schedule.run_pending()
        time.sleep(60)
