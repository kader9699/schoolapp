from connexion import get_connection
import pandas as pd
import bcrypt

def ajouter_parent(nom, prenom, numero, mot_de_passe):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO parents (nom, prenom, numero, mot_de_passe) VALUES (%s, %s, %s, %s)", (nom, prenom, numero, mot_de_passe))
    conn.commit()
    cursor.close()
    conn.close()


def hash_password(password):
    # Générer un sel et hacher le mot de passe
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8') 


def ajouter_eleve(nom, prenom, age, classe_id, parent_id,sexe):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO eleves (nom, prenom,age, classe_id, parent_id,sexe) VALUES (%s, %s, %s, %s,%s,%s)", (nom, prenom,age, classe_id, parent_id,sexe))
    conn.commit()
    cursor.close()
    conn.close()

def ajouter_enseignant(nom, prenom, numero, mot_de_passe, est_directeur=False):
    conn = get_connection()
    cursor = conn.cursor()
    mot_de_passe_s = hash_password(mot_de_passe)
    cursor.execute("INSERT INTO enseignants (nom, prenom, numero, mot_de_passe, est_directeur) VALUES (%s, %s, %s, %s, %s)", (nom, prenom, numero, mot_de_passe, est_directeur))
    conn.commit()
    cursor.close()
    conn.close()

def authentifier_enseignant(prenom, mot_de_passe):
    conn = get_connection()
    cursor = conn.cursor()
    #mot_de_passe_s = hash_password(mot_de_passe)
    cursor.execute("SELECT id, est_directeur,mot_de_passe FROM enseignants WHERE prenom = %s AND mot_de_passe = %s", (prenom, mot_de_passe))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def authentifier_parent(prenom, mot_de_passe):
    conn = get_connection()
    cursor = conn.cursor()
    mot_de_passe_s = hash_password(mot_de_passe)
    cursor.execute("SELECT id, nom FROM parents WHERE prenom = %s AND mot_de_passe = %s", (prenom, mot_de_passe))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result


def ajouter_classe(nom):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO classes (nom) VALUES (%s)", (nom,))
    conn.commit()
    cursor.close()
    conn.close()



def enregistrer_paiement(eleve_id, montant,date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO paiements (eleve_id, montant, date) VALUES (%s, %s, %s)", (eleve_id, montant, date))
    conn.commit()
    cursor.close()
    conn.close()

def enregistrer_absence(eleve_id, date, justifie=False):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO absences (eleve_id, date, justifie) VALUES (%s, %s, %s)", (eleve_id, date, justifie))
    conn.commit()
    cursor.close()
    conn.close()
    
def obtenir_classes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nom FROM classes")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result  

def obtenir_eleves_par_classe(classe_id):
    conn = get_connection()
    query = "SELECT id, nom, prenom FROM eleves WHERE classe_id = %s"
    df = pd.read_sql(query, conn, params=(classe_id,))
    conn.close()
    return df

def obtenir_parents():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nom, prenom,numero FROM parents")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def obtenir_parent_par_telephone(numero_telephone):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM parents WHERE numero = %s", (numero_telephone,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

def obtenir_statistiques_absences():
    conn = get_connection()
    query = """
            SELECT e.nom, e.prenom, COUNT(a.id) as total_absences
            FROM eleves e
            LEFT JOIN absences a ON e.id = a.eleve_id
            GROUP BY e.nom, e.prenom
            ORDER BY total_absences DESC
            """
    df = pd.read_sql(query, conn)
    return df

def obtenir_statistiques_paiements():
    conn = get_connection()
    query = """
            SELECT e.nom, e.prenom, SUM(p.montant) as total_paiements
            FROM eleves e
            LEFT JOIN paiements p ON e.id = p.eleve_id
            GROUP BY e.nom, e.prenom
            ORDER BY total_paiements DESC
            """
    df = pd.read_sql(query, conn)
    conn.close()
    return df
