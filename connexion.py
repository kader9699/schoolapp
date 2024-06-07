import psycopg2

import os
import psycopg2

def get_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),  # Récupère l'adresse du serveur PostgreSQL depuis une variable d'environnement
        port=os.getenv("DB_PORT"),  # Récupère le port du serveur PostgreSQL depuis une variable d'environnement
        database=os.getenv("DB_NAME"),  # Récupère le nom de la base de données depuis une variable d'environnement
        user=os.getenv("DB_USER"),  # Récupère le nom d'utilisateur PostgreSQL depuis une variable d'environnement
        password=os.getenv("DB_PASSWORD")  # Récupère le mot de passe PostgreSQL depuis une variable d'environnement
    )
    return conn

def get_connectione():
    conn = psycopg2.connect(
        host="localhost",
        database="school_management",
        user="kader",
        password="password"
    )
    return conn