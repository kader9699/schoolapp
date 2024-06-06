import streamlit as st
from fonction import authentifier_enseignant, authentifier_parent

# Variables de session pour l'authentification
if 'authentifie' not in st.session_state:
    st.session_state.authentifie = False
if 'est_directeur' not in st.session_state:
    st.session_state.est_directeur = False
if 'est_parent' not in st.session_state:
    st.session_state.est_parent = False

# Fonction d'authentification
def authentifier_utilisateur(prenom, mot_de_passe):
    enseignant = authentifier_enseignant(prenom, mot_de_passe)
    parent = authentifier_parent(prenom, mot_de_passe)
    if enseignant:
        st.session_state.authentifie = True
        st.session_state.est_directeur = enseignant[1]  # utilisateur[1] est True si directeur
        st.session_state.est_parent = False
        st.success("Authentification réussie (Enseignant/Directeur)")
        return True
    elif parent:
        st.session_state.authentifie = True
        st.session_state.est_directeur = False
        st.session_state.est_parent = True
        st.success("Authentification réussie (Parent)")
        return True
    else:
        st.error("Prénom ou mot de passe incorrect")
        return False
