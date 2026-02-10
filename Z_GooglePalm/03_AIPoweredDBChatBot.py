#
#
# pip install -U langchain langchain-community langchain-experimental \
#                langchain-google-genai pymysql python-dotenv streamlit
#
#   Run the below code as
#   streamlit run C:\Rama\Learn\GenerativeAI\Z_GooglePalm\03_AIPoweredDBChatBot.py
#
#  Ask questions like :
#       print all brand names
#       Show brand, color, size, price and discount percent
#       How many t shirts are there for Nike in  extra large size and red color
#####################################
import os
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import io
import re
import ast
import decimal

from langchain_community.utilities import SQLDatabase
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.sql import SQLDatabaseChain
from sqlalchemy import text


## To Clean up SQL else it has lot fo new lines etc which will break the SQL.
def clean_sql(sql: str) -> str:
    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")
    sql = sql.replace("mysql", "")
    sql = sql.replace("SQL", "")
    return sql.strip()

# Load env
#  Save your password in this .env file
# MYSQL_PASSWORD=DB_PASSWORD
# AI_STUDIO_GOOGLE_COM_API_KEY=YOUR_AI_STUDIO_KEY
#
load_dotenv(r"C:\Rama\Learn\AI\.env")

# Connect DB
db = SQLDatabase.from_uri(
    f"mysql+pymysql://root:{os.getenv('MYSQL_PASSWORD')}@localhost:3306/atliq_tshirts"
)

# LLM
llm = ChatGoogleGenerativeAI(
    model="models/gemini-flash-lite-latest",
    google_api_key=os.getenv("AI_STUDIO_GOOGLE_COM_API_KEY"),
    temperature=0
)

# Chain
chain = SQLDatabaseChain.from_llm(
    llm,
    db,
    verbose=True,
    return_sql=True
)

# ---------------- UI ----------------
st.set_page_config(page_title="AI DB Chatbot")
st.title("🤖 AI-Powered MySQL Chatbot")

question = st.text_input("Ask something about your database:")



if st.button("Ask"):
    if question:
        response = chain.invoke({"query": question})

        result_text = response.get("result", "")

        # This is how response looks we need to extract SQLquery form this.
        # { "query": "How many t shirts are there for Nike in extra small size and white color",
        #   "result": "Question: How many t shirts are there for Nike in extra small size and white color"
        #   "SQLQuery: SELECT SUM(`stock_quantity`) FROM t_shirts WHERE `brand` = 'Nike' AND `size` = 'XS' AND `color` = 'White'"
        # }

        match = re.search(r"SQLQuery:\s*(.*)", result_text)
        if not match:
            st.error("Could not extract SQL from model output.")
            st.write(response)
            st.stop()

        sql = match.group(1).strip()

        st.subheader("🧾 Generated SQL")
        st.code(sql, language="sql")

        # Execute SQL properly using SQLAlchemy
        with db._engine.connect() as conn:
            result = conn.execute(text(sql))
            rows = result.fetchall()
            columns = result.keys()
        st.write("DEBUG ROWS:", rows)

        # Convert SQLAlchemy Row objects properly
        clean_rows = [tuple(row) for row in rows]

        df = pd.DataFrame(clean_rows, columns=columns)

        st.subheader("📊 Query Results")

        if not df.empty:
            st.dataframe(df, width="stretch")

            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)

            st.download_button(
                "⬇ Download as CSV",
                csv_buffer.getvalue(),
                file_name="query_results.csv",
                mime="text/csv"
            )
        else:
            st.info("No rows returned.")


