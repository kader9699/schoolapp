import streamlit as st
from dotenv import load_dotenv
from fonction import (obtenir_classes,enregistrer_paiement,
                    enregistrer_absence,enregistrer_paiement,ajouter_classe,
                    ajouter_enseignant,ajouter_eleve,obtenir_parents,
                    ajouter_parent,obtenir_eleves_par_classe,obtenir_parent_par_telephone,
                    obtenir_statistiques_paiements,obtenir_statistiques_absences)
from auth_session import authentifier_utilisateur
load_dotenv()
    
    
# Fonction d'authentification
def afficher_formulaire_authentification():
    st.subheader("Authentification")
    prenom = st.text_input("Prénom")
    mot_de_passe = st.text_input("Mot de passe", type='password')
    if st.button("Se connecter"):
        if not prenom:
            st.error("Le prenom est requis.")
        elif not mot_de_passe:
            st.error("Mot de passe est requis.")
        else:
            authentifier_utilisateur(prenom, mot_de_passe)

def deconnexion():
    st.session_state.authentifie = False
    st.session_state.est_directeur = False
    st.session_state.est_parent = False

# Bouton de déconnexion
if st.session_state.authentifie:
    st.button("Déconnexion", on_click=deconnexion)

if not st.session_state.authentifie:
    afficher_formulaire_authentification()
    
    
else:
    if st.session_state.est_directeur:
        menu = ["Accueil", "Ajouter Classe", "Ajouter Élève", "Ajouter Enseignant", "Ajouter Parent", 
                "Enregistrer Paiement", "Enregistrer Absence", "Visualiser Statistiques"]
    elif st.session_state.est_parent:
        menu = ["Accueil", "Visualiser Présences"]
    else:  # enseignant
        menu = ["Accueil", "Enregistrer Absence", "Visualiser Statistiques"]

    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Accueil":
        st.title("Bienvenue à l'École Coranique Mederesatul Bin Baz!")
        #st.subheader("Bienvenue à l'application de gestion des élèves")

    elif choice == "Ajouter Classe":
        if st.session_state.est_directeur:
            st.subheader("Ajouter une nouvelle classe")
            nom = st.text_input("Nom de la classe")
            if st.button("Ajouter Classe"):
                if not nom:
                    st.error("Le nom est requis.")
                else:
                    ajouter_classe(nom)
                    st.success("Classe ajoutée avec succès")
        else:
            st.error("Vous n'avez pas l'autorisation d'ajouter des classes")

    elif choice == "Ajouter Élève":
        if st.session_state.est_directeur:
            classes_df = obtenir_classes()
            classes_options = [f"{class_info[0]} - {class_info[1]}" for class_info in classes_df]
            st.subheader("Ajouter un nouvel élève")
            nom = st.text_input("Nom de l'élève")
            prenom = st.text_input("Prénom de l'élève")
            age = st.number_input("Age de l'lève", min_value=1)
            sexe = st.radio("Sexe de l'élève", ["Masculin", "Féminin"])
            classe_selectionnee = st.selectbox("Nom de la classe", classes_options)
            numero_telephone_parent = st.text_input("Numéro de téléphone du parent")
            if classe_selectionnee is not None:
                classe_id = int(classe_selectionnee.split(" - ")[0]) 

            # Si l'utilisateur clique sur le bouton pour ajouter l'élève
            if st.button("Ajouter Élève"):
                # Vérifier que tous les champs sont remplis
                if not nom:
                    st.error("Le nom est requis.")
                elif not prenom:
                    st.error("Le prénom est requis.")
                elif not age:
                    st.error("L'âge est requis.")
                elif not sexe:
                    st.error("Le sexe est requis.")
                elif not classe_selectionnee:
                    st.error("La classe est requise.")
                elif not numero_telephone_parent:
                    st.error("Le numéro de téléphone du parent est requis.")
                else:
                    # Obtenir l'ID du parent à partir du numéro de téléphone
                    parent_id = obtenir_parent_par_telephone(numero_telephone_parent)
                    # Si aucun parent n'est trouvé avec ce numéro de téléphone
                    if parent_id is None:
                        st.error("Aucun parent trouvé avec ce numéro de téléphone.")
                    else:
                        # Ajouter le nouvel élève à la base de données avec l'ID du parent
                        ajouter_eleve(nom, prenom, age, classe_id, parent_id,sexe)
                        st.success("Élève ajouté avec succès")
        else:
            st.error("Vous n'avez pas l'autorisation d'ajouter des élèves")

    elif choice == "Ajouter Enseignant":
        if st.session_state.est_directeur:
            st.subheader("Ajouter un nouvel enseignant")
            nom = st.text_input("Nom de l'enseignant")
            prenom = st.text_input("Prénom de l'enseignant")
            numero = st.text_input("Numero de l'enseignant")
            mot_de_passe = st.text_input("Mot de passe", type='password')
            est_directeur = st.checkbox("Directeur")
            if st.button("Ajouter Enseignant"):
                # Vérifier que tous les champs sont remplis
                if not nom:
                    st.error("Le nom est requis.")
                elif not prenom:
                    st.error("Le prénom est requis.")
                elif not mot_de_passe:
                    st.error("Mot de passe est requis.")
                elif not numero:
                    st.error("Numero  est requis.")
                else:
                    ajouter_enseignant(nom, prenom, numero, mot_de_passe, est_directeur)
                    st.success("Enseignant ajouté avec succès")
        else:
            st.error("Vous n'avez pas l'autorisation d'ajouter des enseignants")

    elif choice == "Ajouter Parent":
        if st.session_state.est_directeur:
            st.subheader("Ajouter un nouveau parent")
            nom = st.text_input("Nom du parent")
            prenom = st.text_input("Prénom du parent")
            numero = st.text_input("Numero du parent")
            mot_de_passe = st.text_input("Mot de passe", type='password')
            if st.button("Ajouter Parent"):
                if not nom:
                    st.error("Le nom est requis.")
                elif not prenom:
                    st.error("Le prénom est requis.")
                elif not numero:
                    st.error("Numero est requis.")
                elif not mot_de_passe:
                    st.error("Mot de passe est requis.")
                else:
                    ajouter_parent(nom, prenom, numero, mot_de_passe)
                    st.success("Parent ajouté avec succès")
        else:
            st.error("Vous n'avez pas l'autorisation d'ajouter des parents")

    elif choice == "Enregistrer Paiement":
        st.subheader("Enregistrer un paiement")
        eleve_id = st.number_input("ID de l'élève", min_value=1)
        montant = st.number_input("Montant du paiement", min_value=0.0)
        date = st.date_input("Date du paiement")
        if st.button("Enregistrer Paiement"):
            enregistrer_paiement(eleve_id, montant, date)
            st.success("Paiement enregistré avec succès")

    elif choice == "Enregistrer Absence":
        st.subheader("Enregistrer une absence")

        # Obtenir la liste des classes
        classes_df = obtenir_classes()
        classes_options = classes_df.apply(lambda row: f"{row['id']} - {row['nom']}", axis=1).tolist()
        
        classe_selection = st.selectbox("Sélectionner la classe", classes_options)
        
        # Extraire l'ID de la classe sélectionnée
        classe_id = int(classe_selection.split(" - ")[0])
        
        # Obtenir la liste des élèves de la classe sélectionnée
        eleves_df = obtenir_eleves_par_classe(classe_id)
        eleves_options = eleves_df.apply(lambda row: f"{row['id']} - {row['nom']} {row['prenom']}", axis=1).tolist()
        
        eleve_selection = st.selectbox("Sélectionner l'élève", eleves_options)
        
        # Extraire l'ID de l'élève sélectionné
        eleve_id = int(eleve_selection.split(" - ")[0])
        
        date = st.date_input("Date de l'absence")
        justifie = st.checkbox("Justifié")
        
        if st.button("Enregistrer Absence"):
            enregistrer_absence(eleve_id, date, justifie)
            st.success("Absence enregistrée avec succès")

    elif choice == "Visualiser Statistiques":
        st.subheader("Visualiser les statistiques")

        absences_df = obtenir_statistiques_absences()
        paiements_df = obtenir_statistiques_paiements()

        st.subheader("Taux d'absences par élève")
        st.dataframe(absences_df)
        st.bar_chart(absences_df.set_index(['nom', 'prenom']))

        st.subheader("Taux de paiements par élève")
        st.dataframe(paiements_df)
        st.bar_chart(paiements_df.set_index(['nom', 'prenom']))