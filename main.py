import streamlit as st
import random

#https://pythonwife.com/streamlit-interview-questions/

st.title("Etude sur le provisionnement en assurance non-vie")


#Year = [1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010]
#Unemployment_Rate = [9.8, 12, 8, 7.2, 6.9, 7, 6.5, 6.2, 5.5, 6.3]


#import altair as alt
#import pandas as pd

#data = {"annee":Year,"taux":Unemployment_Rate}
#datafr = pd.DataFrame(data)


#chart1 = alt.Chart(datafr).mark_line(size=10).encode(
#    x='annee',
#    y='taux',
#    color='Origin:N',
#    tooltip=['taux']
#).interactive()

#chart1

#donnees = [20,40,50,20,20,30,20,40,50]
#st.line_chart(donnees)

#import time
#my_bar = st.progress(0)
#for percent_complete in range(100):
#    time.sleep(0.001)
#    my_bar.progress(percent_complete + 1)

#Début de l'étude
if 'page' not in st.session_state:

    st.session_state.user_data = []
    st.session_state.page = 1

    import socket
    st.session_state.user_data.append(socket.gethostbyname(socket.gethostname()))

    from datetime import datetime
    from datetime import date

    date_deb = date.today()
    date_deb2 = date_deb.strftime("%d/%m/%Y")
    st.session_state.user_data.append(date_deb2)

    now = datetime.now()
    temps_debut = now.strftime("%H:%M:%S")
    st.session_state.user_data.append(temps_debut)

    st.write("Ce bref questionnaire vise à obtenir une meilleure connaissance des pratiques actuarielles dans le domaine du provisionnement non-vie. "
             "Actuaires, chargés d’études actuarielles et étudiants en actuariat sont invités à y participer.")
    st.write("Les résultats sont anonymes, les informations personnelles servant uniquement à des fins de statistiques descriptives.")
    st.write("Merci d’avance pour votre participation,")
    st.button("Commencer l'étude")

#Profil de l'individu
elif st.session_state.page==1:

    st.header("Informations générales")
    st.write("Ce premier groupe de question vise à préciser votre profil")

    with st.form(key='bloc_1'):
        sexe = st.selectbox('Sexe', ["-", "Homme", "Femme", "Non précisé"])
        age = st.selectbox('Âge', ["-","18-25", "26-35", "35-50", "51 et plus"])
        type_entreprise = st.selectbox("Type d'entreprise",["-", "Ne travaille pas", "Compagnie d'assurance", "Mutuelle","Bancassureur","Cabinet de conseil","Autre"])
        seniorite = st.selectbox("Séniorité en actuariat",["-","Etudiant","0-2 ans","2-5 ans","5-8 ans","8-15 ans","15 ans et plus"])
        submit_button_1 = st.form_submit_button(label='Page suivante')

    if submit_button_1:
        st.session_state.page += 1

        st.session_state.user_data.append("BLOC")

        st.session_state.user_data.append("Sexe")
        st.session_state.user_data.append(sexe)
        st.session_state.user_data.append("Age")
        st.session_state.user_data.append(age)
        st.session_state.user_data.append("Type d'entreprise")
        st.session_state.user_data.append(type_entreprise)
        st.session_state.user_data.append("Séniorité")
        st.session_state.user_data.append(seniorite)

        st.experimental_rerun()

#Méthodes de provisionnement
elif st.session_state.page==2:

    st.header("Provisionnement")

    with st.form(key='methode_provisionnement'):
        methode_connue = st.multiselect(
            "De quelles méthodes de provisionnement avez déjà entendu parler ? (plusieurs réponses possibles)",
            ["Chain Ladder", "London Chain", "Loss ratio", "Mack", "GLM", "Bornhuetter Ferguson"]) #6 méthodes
        methode_utilisee = st.multiselect(
            "Quelles méthodes avez-vous déjà utilisé dans un cadre professionnel ? (plusieurs réponses possibles)",
            ["Chain Ladder", "London Chain", "Loss ratio", "Mack", "GLM", "Bornhuetter Ferguson"]) #6 méthodes
        sb_methode_provisionnement = st.form_submit_button(label="Page suivante")

    if sb_methode_provisionnement:

        st.session_state.page += 1

        while len(methode_connue)<6:
            methode_connue.append("")
        while len(methode_utilisee)<6:
            methode_utilisee.append("")

        st.session_state.user_data.append("BLOC")

        st.session_state.user_data.append("Méthodes connues")
        st.session_state.user_data.extend(methode_connue)

        st.session_state.user_data.append("Méthodes utilisees")
        st.session_state.user_data.extend(methode_utilisee)

        st.session_state.user_data.append("BLOC")

        #GROUPE QUESTION SUIVANTE
        st.session_state.alea = random.uniform(0, 1)
        st.session_state.user_data.append(st.session_state.alea)
        if st.session_state.alea < 0.5:
            st.session_state.user_data.append("Framing positif")
        else:
            st.session_state.user_data.append("Framing négatif")
        #GROUPE QUESTION SUIVANTE

        st.experimental_rerun()

#Maladie Kahneman
elif st.session_state.page==3:

    st.header("Approche du risque")
    st.write("Ce deuxième groupe de questions vise à étudier votre appréhension du risque")

    if st.session_state.alea < 0.5:
        with st.form(key="test_framing_kahneman"):
            st.write("La France s'attend à l'arrivée d'une maladie infectieuse, supposée tuer 600 personnes. Deux programmes de traitement sont disponibles pour endiguer la maladie :")
            st.write("- Si le programme A est adopté, 200 personnes seront sauvées")
            st.write("- Si le programme B est adopté, il y a 1/3 de chances que 600 personnes soient sauvées et 2/3 de chances que personne ne soit sauvé")
            programme = st.selectbox("Quel programme vous semble préférable ?",["-", "Programme A", "Programme B"])
            sb_framing_kahneman = st.form_submit_button(label="Page suivante")

    else:
        with st.form(key="test_framing_kahneman"):
            st.write("La France s'attend à l'arrivée d'une maladie infectieuse, supposée tuer 600 personnes. Deux programmes de traitement sont disponibles pour endiguer la maladie :")
            st.write("- Si le programme A est adopté, 400 personnes mourront")
            st.write(" - Si le programme B est adopté, il y a 1/3 de chances que personne ne meure et 2/3 de chances que 600 personnes meurent")
            programme = st.selectbox("Quel programme vous semble préférable ?", ["-", "Programme A", "Programme B"])
            sb_framing_kahneman = st.form_submit_button(label="Page suivante")

    if sb_framing_kahneman:
        st.session_state.page += 1
        st.session_state.user_data.append(programme)
        st.experimental_rerun()

#Gambler's fallacy
elif st.session_state.page==4:

    st.header("Approche du risque")

    with st.form(key="gambler"):
        st.write("On estime la probabilité d’avoir un accident non responsable à 2% pour les individus en portefeuille. Les assurés A et B ont le même profil de risque et les mêmes pratiques de conduite. ")
        st.write("L’année dernière, l’individu A a eu 4 accidents auto non responsables. L’individu B n’a jamais eu d’accident")
        accident = st.text_input("Qui est le plus susceptible d'avoir un nouvel accident le premier ?")
        sb_gambler = st.form_submit_button(label="Page suivante")

    if sb_gambler:
        st.session_state.page += 1
        st.session_state.user_data.append("Individu accident")
        st.session_state.user_data.append(accident)
        st.experimental_rerun()

#Intervalle de confiance S/P auto
elif st.session_state.page==5:

    st.header("Marché assurantiel")

    with st.form(key="marche_auto"):
        st.write("Donnez un intervalle pour le ratio S/P du secteur automobile français en 2019 avec une certitude de 90%")
        marche_auto = st.slider("Ratio S/P du secteur automobile français",min_value=50,max_value=150,value=(90,110))
        sb_SP_marche_auto = st.form_submit_button(label="Page suivante")

    if sb_SP_marche_auto:

        st.session_state.page += 1
        st.session_state.user_data.append("Ratio S/P du marché automobile en 2020")
        st.session_state.user_data.extend(marche_auto)

        #GROUPE QUESTION SUIVANTE
        st.session_state.alea = random.uniform(0, 1)
        st.session_state.user_data.append(st.session_state.alea)
        if st.session_state.alea < 0.5:
            st.session_state.user_data.append("Ancre : 54%")
        else:
            st.session_state.user_data.append("Ancre : 124%")
        #GROUPE QUESTION SUIVANTE

        st.experimental_rerun()

#Position par rapport à l'ancre MRH
elif st.session_state.page==6:

    st.header("Marché assurantiel")

    if st.session_state.alea < 0.5 :
        with st.form(key="marche_MRH"):
            st.write("A votre avis, le ratio combiné comptable du secteur de l'assurance multirisque habitation en France en 2020 (avant réassurance) était-il supérieur ou inférieur à 54% ?")
            ancre_MRH = st.selectbox(" ",["-", "Supérieur", "Inférieur"])
            sb_position_ancre = st.form_submit_button(label="Page suivante")

    else :

        with st.form(key="marche_MRH"):
           st.write("A votre avis, le ratio combiné comptable du secteur de l'assurance multirisque habitation en France en 2020 (avant réassurance) était-il supérieur ou inférieur à 124% ?")
           ancre_MRH = st.selectbox(" ",["-", "Supérieur", "Inférieur"])
           sb_position_ancre = st.form_submit_button(label="Page suivante")

    if sb_position_ancre:

        st.session_state.page += 1
        st.session_state.user_data.append("Position vis à vis de l'ancre")
        st.session_state.user_data.append(ancre_MRH)

        st.experimental_rerun()

#Ratio S/P MRH
elif st.session_state.page == 7:

    st.header("Marché assurantiel")

    if st.session_state.alea < 0.5:

        with st.form(key="marche_MRH"):
            st.write( "A combien estimeriez-vous ce ratio S/P ?")
            marche_MRH = st.slider("Ratio S/P MRH (2020)", min_value=20, max_value=160, value=54)
            sb_ancre_MRH = st.form_submit_button(label="Page suivante")

    else :

        with st.form(key="marche_MRH"):
            st.write( "A combien estimeriez-vous ce ratio S/P ?")
            marche_MRH = st.slider("Ratio S/P MRH (2020)", min_value=20, max_value=160, value=124)
            sb_ancre_MRH = st.form_submit_button(label="Page suivante")

    if sb_ancre_MRH:

        st.session_state.page += 1

        st.session_state.user_data.append("Ratio S/P MRH en 2020")
        st.session_state.user_data.append(marche_MRH)

        st.session_state.alea = random.uniform(0, 1)
        st.session_state.user_data.append(st.session_state.alea)
        if st.session_state.alea < 0.5:
            st.session_state.user_data.append("Comparaison auto - terrorisme")
        else:
            st.session_state.user_data.append("Comparaison auto - ")

        st.experimental_rerun()

#Page à déterminer
elif st.session_state.page == 8:

    st.header("Marché assurantiel")

    if st.session_state.alea < 0.5:

        with st.form(key="marche_MRH"):
            st.write( "A combien estimeriez-vous ce ratio S/P ?")
            marche_MRH = st.slider("Ratio S/P MRH (2020)", min_value=54, max_value=114, value=64)
            submit_button_6 = st.form_submit_button(label="Page suivante")

    else :

        with st.form(key="marche_MRH"):
            st.write( "A combien estimeriez-vous ce ratio S/P ?")
            marche_MRH = st.slider("Ratio S/P MRH (2020)", min_value=64, max_value=134, value=114)
            submit_button_6 = st.form_submit_button(label="Page suivante")

    if submit_button_6:
        st.session_state.page += 1
        st.session_state.user_data.append("Ratio S/P MRH en 2020")
        st.session_state.user_data.append(marche_MRH)
        st.experimental_rerun()

#Remarques
elif st.session_state.page == 9:

    with st.form(key='my_form_end'):
        retour_utilisateur = st.text_input(label='Vous pouvez noter ici des remarques éventuelles')
        mail_utilisateur = st.text_input("Vous pouvez noter ici votre adresse mail si vous souhaitez participer à la partie pratique de l'étude (application de la méthode de Chain-Ladder à des cas concrets)", 'E-mail')
        submit_button_end = st.form_submit_button(label="Terminer l'étude")

    if submit_button_end:

        st.session_state.user_data.append(retour_utilisateur)
        st.session_state.user_data.append(mail_utilisateur)

        from datetime import datetime
        from datetime import date
        end = datetime.now()
        temps_fin = end.strftime("%H:%M:%S")
        st.session_state.user_data.append(temps_fin)

        import gspread

        # A supprimer (compromis & modifés)
        credentials = {
            "type": "service_account",
            "project_id": "acoustic-mix-331213",
            "private_key_id": "28bf926ad27ea160b487b68d615b6a8c87659cfa",
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEugIBADANBgkqhkiG9w0BAQEFAASCBKQwggSgAgEAAoIBAQC5enym8sKaQvSb\nLBPjfRg0fZVL6ToQNMvUBTJdMqDHRzBF1d83XwdCoyu/LfOjuGa08SF56Lf5X9K+\nNGzgU/g0tir8GjI+Y0cGl9GYmOjVhN60F669jhvyhDTpDSE1dvoHhrwuRT+tbk5X\nvHR6irx0W/+0y87Qc0SnQBlLwm4HpRWTe8aSwY1huc/Y8Drj9akOh5Z8FJJC2imk\nQrzDu4lFeiAjUgyV2lhuWymNIlVeSd7E4vEMOjtpYH7NakFhgNyklDqobZYCZpFZ\nm23v5HU8llg17mOLpopAWGMHBeHsqhYibk3G6AYPhIk/By3Zl0U/F005nGNrduJJ\nv2rd67lZAgMBAAECgf9KDSfMql9yTLPGwB0GAOEJE+/naYD6YhnULGmki/IPndHI\nD/tulUzGGMn+f3omg24oukeDRJvZvvLaEv7lEUv8v5Op00umsjxJMD6eOMO80QTu\nd1tskrArGF2Hg5Zz92xw/3oM1IOihR0CKluBZqKW/PllACSHVNNeyFimcUSSCB01\nACIFb57ubd9jmfYCHXnDSQdZRT8kuXaOboZ54OcVYhZfaiU2uj3vj8ZyS2PG39jm\nOmeRpDZGf+YWHB41SvvFQwWR1irzQ1G4awCwBHdoa4W8dlh+tcwHPJqaVMb3HCk8\nWlbmMZMQhRaSE4CeUel2WXt3Zu1E9uhNKYmPpYECgYEA86c8ZKsoDoO0MUwLrYNa\nGhFQDv1VoWlif3Ljn7ki4PhdhgUzhh0MTxH0yTZtgubUBN/yhoVxhwBXwuKCLEQx\nqt3Kbxpe65LXSqxVr6gkJn57DZvQqc1F28YWrMONGYGxvBr6ZMIQngRkXy8W3f+2\njF4aPuaoS8u8HqtwSvFSw4ECgYEAwuCVxxTTD4g3KROVt5P4y02MYDuEkoNWNfXw\nmSZjhxrS6WsHan6M0R5GVKFBSUK42pC9JMyXXk+qefRHD9SVXhNm27xU1BabpXqw\nXUW3yBgJuXXw2oQbspOi9Zh7EPAAR6FaDH8s1ysjHxYaFSEvOwq0WZzRgLRaNC9o\nDbpAgdkCgYBqsnJc9yKccIpJCC8Y9atQPQKc/c0w2PBcNVh+ilk+wSRbWw28Dh5k\nxc03C9GbADAaTmNrCyay4rCL1BsC/X3ugB901cx5Rp1mwt7nBC+Id9y1EeWnZg/Q\ndQda8mtonwXRBNNfqigSuoOltv5BiwhKoa7GmsVaI8ame5a6CsGegQKBgD8dD0UH\nmId6PSsffaiT0sq9Fc6A2CG/SWd2fHKNPUSfSllwYVl7HM4JOQvlochBRK78m1VU\nsV1I/dQ7adxVo/5w2CooJ2z82XHRd1bt4mR6bIPVD6klifbe27MgrBLDN8P7HLfZ\nZENXZCuIM/BN7Ab6I4i2Qh+lyWUHSXLQtF2ZAoGAPzJtUNV0j0gAiKv0T6Zl9tzf\nebQn3FwhC1JCWuZj3i2YKboSWW/P67HZTHU0pUVWkdL1TFyFXeshI807ah5980G6\nYfmFSXIB1hDHv60WEDvyMU/zA4y64mCOPht0genVN5RLVRkfEhdAVVu+WfN3YTFf\nrH2CeEEMikMTvo/jHKU=\n-----END PRIVATE KEY-----\n",
            "client_email": "testteam@acoustic-mix-331213.iam.gserviceaccount.com",
            "client_id": "103380036233115407551",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/testteam%40acoustic-mix-331213.iam.gserviceaccount.com"
        }

        # credentials_2 = {
        #    "type": st.secrets["s_type"],
        #    "project_id": st.secrets["s_project_id"],
        #    "private_key_id": st.secrets["s_private_key_id"],
        #    "private_key": st.secrets["s_private_key"],
        #    "client_email": st.secrets["s_client_email"],
        #    "client_id": st.secrets["s_client_id"],
        #    "auth_uri": st.secrets["s_auth_uri"],
        #    "token_uri": st.secrets["s_token_uri"],
        #    "auth_provider_x509_cert_url": st.secrets["s_auth_provider_x509_cert_url"],
        #    "client_x509_cert_url": st.secrets["s_client_x509_cert_url"]
        # }

        gc = gspread.service_account_from_dict(credentials)
        sh = gc.open("test_beta")
        worksheet = sh.sheet1
        worksheet.insert_row(st.session_state.user_data, 1)

        st.session_state.page = 999
        st.experimental_rerun()

#Page de fin
elif st.session_state.page == 999:

    st.write("Vos résultats ont bien été pris en compte")
    st.write("Merci pour votre participation")
    st.write("Pour toute remarque ou commentaire complémentaire, n'hésitez pas à envoyer un mail à rchabert@deloitte.fr")

#my_bar.empty()

