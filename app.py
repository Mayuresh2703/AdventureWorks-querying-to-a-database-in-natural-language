import streamlit as st
import pyodbc as odbc
import pandas as pd
from dotenv import load_dotenv
import openai

with st.sidebar:
    st.header("Interact with Database")
    st.markdown("""
    ## About 
    Works with the help of OpenAI""")
    st.write("For Reference")
    st.write('''-[Streamlit](https://streamlit.io/) 
            -  [OpenAI](https://platform.openai.com/docs/models)''')

def main():
    load_dotenv()
    st.header("AdventureWorks querying to a database in Natural Language")
    DRIVER_NAME='ODBC Driver 17 for SQL Server'
    SERVER_NAME='DESKTOP-RPSH2LU\SQLEXPRESS'
    DATABASE_NAME='AdventureWorks2019'

    connection_string=("Driver={ODBC Driver 17 for SQL Server};"
            "Server=DESKTOP-RPSH2LU\\SQLEXPRESS;"
            "Database=AdventureWorks2019;"
            "Trusted_Connection=yes;")

    cnxn = odbc.connect(connection_string)
    cursor=cnxn.cursor()
    cursor1=cnxn.cursor()
    cursor2=cnxn.cursor()
    a=cursor.execute("SELECT concat (Table_schema,'.',Table_name) FROM information_schema.tables")
    st.write("Connection Established")
    
    option = st.selectbox("Select Your Table", options=a.fetchall())
    if not option:
        st.write("Choose your option")
    else:
        st.write("Table Chosen", option)

        option = str(option).strip('(').strip(')').strip(',')
        st.markdown(f"## {option}")
        option1 = str(option).split(".")[1].strip("'")

        b = cursor2.execute(f"SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{option1}'")
        columns = [item[0] for item in b.fetchall()]
        selected_column = st.radio("Columns", options=columns)

        query = st.text_input("Write your query")
        if query:
            prompt = f"Generate a SQL server query to retrieve {query} from the database with table {option} and column {selected_column}"
            response = openai.Completion.create(engine='text-davinci-003', prompt=prompt, max_tokens=100)
            query = response.choices[0].text.strip()
            st.write(query)

            result = cursor1.execute(query)
            field_names = [i[0] for i in cursor1.description]

            df = pd.DataFrame(result.fetchall())
            st.write(field_names)
            df[0] = df[0].astype(str)
            columns = df[0].str.split(',', expand=True)
            new_df = pd.DataFrame(columns)
            st.write(new_df)
        else:
            pass

if __name__ == '__main__':
    main()
