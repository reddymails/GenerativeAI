import os
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.sql import SQLDatabaseChain

# Load env file
load_dotenv(r"C:\Rama\Learn\AI\.env")

mysql_password = os.getenv("MYSQL_PASSWORD")
if not mysql_password:
    raise RuntimeError("MYSQL_PASSWORD not found in .env")

# Build connection string
db_uri = f"mysql+pymysql://root:{mysql_password}@localhost:3306/atliq_tshirts"

# Connect
db = SQLDatabase.from_uri(db_uri)

# Test connection
print("Connected!")
print("Tables:", db.get_usable_table_names())

print(db.run("SELECT * FROM t_shirts LIMIT 5;"))

#############
##  I am using free tire ones here
## you can always switch to different models (Print models using 01_ListGoogleModelInYourRegion.py)
## models/gemini-flash-latest
# models/gemini-flash-lite-latest
#############
llm = ChatGoogleGenerativeAI(
    model="models/gemini-flash-latest",
    google_api_key=os.getenv("AI_STUDIO_GOOGLE_COM_API_KEY"),
)

chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

# response = chain.invoke({"query": "Show top 5 brands by  Stock"})
# print(response["result"])

response = chain.invoke({"query": "Show Top Discount along with brand"})
print(response["result"])
