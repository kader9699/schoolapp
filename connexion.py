import psycopg2
import streamlit as st
import ossaudiodev
import os

def get_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        st.write("Connexion à la base de données réussie")
        return conn
    except Exception as e:
        st.error(f"Erreur de connexion à la base de données : {e}")
        return None



def get_connectione():
    conn = psycopg2.connect(
        host="localhost",
        database="school_management",
        user="kader",
        password="password"
    )
    return conn