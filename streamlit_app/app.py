# streamlit_app/app.py
import streamlit as st
import pandas as pd
import psycopg2
import os

# Get database connection parameters from environment variables
DATABASE_URL = os.getenv('DATABASE_URL')

def get_connection():
    return psycopg2.connect(DATABASE_URL)

def create_table():
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute('''
            CREATE TABLE IF NOT EXISTS data (
                id SERIAL PRIMARY KEY,
                value TEXT NOT NULL
            )
        ''')
        conn.commit()
    conn.close()

def insert_data(value):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute('INSERT INTO data (value) VALUES (%s)', (value,))
        conn.commit()
    conn.close()

def get_data():
    conn = get_connection()
    df = pd.read_sql('SELECT * FROM data', conn)
    conn.close()
    return df

# Create table if it doesn't exist
create_table()

st.title("Streamlit App with PostgreSQL")

value = st.text_input("Enter a value:")
if st.button("Submit"):
    insert_data(value)
    st.success("Data submitted!")

st.subheader("Stored Data")
data = get_data()
st.write(data)
