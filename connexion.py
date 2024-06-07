import psycopg2
import streamlit as st
import os

def get_connection():
    try:
        conn = psycopg2.connect(
            host="dpg-cph3jmug1b2c73b8nm50-a.frankfurt-postgres.render.com",
            port=5432,
            database="school_management_jqmv",
            user="kader",
            password="C2TyF6bJtKxtEsSWP2o0tjYOBv1e0HbB"
        )
        return conn
    except Exception as e:
        st.error(f"Erreur de connexion à la base de données : {e}")
        return None
    
def get_connectione():
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


