import streamlit as st
import random
import altair as alt
import pandas as pd

# https://pythonwife.com/streamlit-interview-questions/

st.title("Etude sur le provisionnement en assurance non-vie")

if 'menu' not in st.session_state:

    st.session_state.menu = 0   # 0 menu, 1 questionnaire, 2 cas pratique

    from datetime import datetime
    from datetime import date
    import gspread

    ouverture = datetime.now()
    temps_fin = ouverture.strftime("%H:%M:%S")

    credentials = {
        "type": st.secrets["s_type"],
        "project_id": st.secrets["s_project_id"],
        "private_key_id": st.secrets["s_private_key_id"],
        "private_key": st.secrets["s_private_key"],
        "client_email": st.secrets["s_client_email"],
        "client_id": st.secrets["s_client_id"],
        "auth_uri": st.secrets["s_auth_uri"],
        "token_uri": st.secrets["s_token_uri"],
        "auth_provider_x509_cert_url": st.secrets["s_auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["s_client_x509_cert_url"]
    }

    gc = gspread.service_account_from_dict(credentials)
    sh = gc.open("Ouvertures")
    worksheet = sh.sheet1
    worksheet.insert_row(ouverture, 1)

# Début de l'étude

if st.session_state.menu == 0:

    st.write("Cette étude, effectuée dans le cadre d'un mémoire d'actuariat, vise à obtenir une meilleure connaissance des pratiques actuarielles en matière de provisionnement en assurance non-vie.")
    st.write("Professionnels et étudiants dans le domaine de l'actuariat sont invités à y répondre.")
    st.markdown("L'étude est constituée de deux parties indépendantes : un questionnaire en ligne _(~ 5 minutes)_ et un cas pratique sous Excel _(~ 20 minutes)_.")
    st.markdown("L'étude est constituée de deux parties indépendantes :")

    col1, col2 = st.columns(2)

    with col1:
        st.write("- Un questionnaire en ligne")

    with col2:
        st.session_state.questionnaire = st.button("Questionnaire")

    col3, col4 = st.columns(2)

    with col3:
        st.write("- Un cas pratique sous Excel")

    with col4:
        st.session_state.cas_pratique = st.button("Cas pratique")

    st.markdown("**Merci par avance pour votre participation !**")

    st.markdown("Pour toute remarque ou commentaire, n'hésitez pas à contacter Romain Chabert à l'adresse <a href='mailto:rchabert@deloitte.fr'>rchabert@deloitte.fr</a>.", unsafe_allow_html=True)

    if st.session_state.questionnaire:
        st.session_state.menu = 1
        st.session_state.page = 0
        st.experimental_rerun()

    if st.session_state.cas_pratique:
        st.session_state.menu = 2
        st.experimental_rerun()

elif st.session_state.menu == 1:

    if st.session_state.page == 0:

        st.write("Ce questionnaire est constitué d'une dizaine de questions, pour lesquelles il sera demandé de sélectionner une ou plusieurs réponses, de l'écrire ou de sélectionner celle-ci sur une frise.")
        st.write("Les résultats du questionnaire sont anonymes, les informations personnelles servant uniquement à des fins de statistiques descriptives.")
        st.markdown("_Attention : une fois le questionnaire commencé il n'est pas possible de revenir en arrière._")
        st.session_state.deb_questionnaire = st.button("Commencer le questionnaire")
        st.session_state.retour_menu = st.button("Retour")

        if st.session_state.deb_questionnaire:
            st.session_state.page = 1
            st.experimental_rerun()

        if st.session_state.retour_menu:
            st.session_state.menu = 0
            st.experimental_rerun()

    # Profil de l'individu
    elif st.session_state.page == 1:

        st.session_state.user_data = []

        from datetime import datetime
        from datetime import date

        date_deb = date.today()
        date_deb2 = date_deb.strftime("%d/%m/%Y")
        st.session_state.user_data.append(date_deb2)

        now = datetime.now()
        temps_debut = now.strftime("%H:%M:%S")
        st.session_state.user_data.append(temps_debut)

        st.header("Informations générales")
        st.write("Ce premier groupe de question vise à préciser votre profil")

        with st.form(key='bloc_1'):
            mail_utilisateur = st.text_input("Adresse e-mail", '@')
            sexe = st.selectbox('Sexe', ["-", "Homme", "Femme", "Non précisé"])
            age = st.selectbox('Âge', ["-", "18-25", "26-35", "35-50", "51 et plus"])
            type_entreprise = st.selectbox("Type d'entreprise", ["-", "Étudiant", "Compagnie d'assurance", "Mutuelle", "Bancassureur", " Cabinet de conseil", "Autre"])
            seniorite = st.selectbox("Séniorité en actuariat", ["-", "Étudiant", "0-2 ans", "2-5 ans", "5-8 ans", "8-15 ans", "15 ans et plus"])
            submit_button_1 = st.form_submit_button(label='Page suivante')

        if submit_button_1:

            if mail_utilisateur == "@" or mail_utilisateur == "":
                st.warning("Merci de bien vouloir renseigner votre adresse e-mail")

            else:
                st.session_state.page += 1

                st.session_state.user_data.append("BLOC")
                st.session_state.user_data.append("Adresse mail")
                st.session_state.user_data.append(mail_utilisateur)
                st.session_state.user_data.append("Sexe")
                st.session_state.user_data.append(sexe)
                st.session_state.user_data.append("Age")
                st.session_state.user_data.append(age)
                st.session_state.user_data.append("Type d'entreprise")
                st.session_state.user_data.append(type_entreprise)
                st.session_state.user_data.append("Séniorité")
                st.session_state.user_data.append(seniorite)

                st.experimental_rerun()

    # Méthodes de provisionnement
    elif st.session_state.page == 2:

        st.header("Provisionnement")

        with st.form(key='methode_provisionnement'):
            provisionnement = st.selectbox('Travaillez-vous ou avez-vous déjà travaillé sur des questions de provisionnement ?', ["-", "Oui", "Non"])
            methode_connue = st.multiselect(
                "De quelles méthodes de provisionnement avez déjà entendu parler ? (plusieurs réponses possibles)",
                ["Chain Ladder", "London Chain", "Loss ratio", "Mack", "GLM", "Bornhuetter Ferguson"])  # 6 méthodes
            methode_utilisee = st.multiselect(
                "Quelles méthodes avez-vous déjà utilisé régulièrement dans un cadre professionnel ? (plusieurs réponses possibles)",
                ["Chain Ladder", "London Chain", "Loss ratio", "Mack", "GLM", "Bornhuetter Ferguson"])  # 6 méthodes
            sb_methode_provisionnement = st.form_submit_button(label="Page suivante")

        if sb_methode_provisionnement:

            st.session_state.page += 1

            while len(methode_connue) < 6:
                methode_connue.append("")
            while len(methode_utilisee) < 6:
                methode_utilisee.append("")

            st.session_state.user_data.append("BLOC")

            st.session_state.user_data.append("Expérience provisionnement")
            st.session_state.user_data.append(provisionnement)

            st.session_state.user_data.append("Méthodes connues")
            st.session_state.user_data.extend(methode_connue)

            st.session_state.user_data.append("Méthodes utilisees")
            st.session_state.user_data.extend(methode_utilisee)

            st.session_state.user_data.append("BLOC")

            # GROUPE QUESTION SUIVANTE
            st.session_state.alea = random.uniform(0, 1)
            st.session_state.user_data.append(st.session_state.alea)
            if st.session_state.alea < 0.5:
                st.session_state.user_data.append("Courbe verte")
            else:
                st.session_state.user_data.append("Courbe rouge")

            st.session_state.alea2 = random.uniform(0, 1)
            st.session_state.user_data.append(st.session_state.alea2)
            if st.session_state.alea2 < 0.5:
                st.session_state.user_data.append("Ancre basse")
            else:
                st.session_state.user_data.append("Ancre haute")

            # GROUPE QUESTION SUIVANTE

            st.experimental_rerun()

    # Evolution du montant de primes (framing)
    elif st.session_state.page == 3:

        st.header("Evolution du montant de primes")

        annee_evol_primes = [1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010]
        valeur_evol_primes = [252.32, 245.46, 243.89, 247.74, 249.43, 244.71, 257.31, 249.67, 252.28, 256.69, 254.42,
                              256.13, 262.21]
        data_evol_primes = {"Annee": annee_evol_primes, "Montant de prime": valeur_evol_primes}
        dataframe_evol_primes = pd.DataFrame(data_evol_primes)

        nearest_prime = alt.selection(type='single', nearest=True, on='mouseover',
                                      fields=['Annee'], empty='none')

        if st.session_state.alea < 0.5:
            # The basic line
            line_prime = alt.Chart(dataframe_evol_primes).mark_line(strokeWidth=6, color='mediumseagreen').encode(
                x=alt.X('Annee:T', scale=alt.Scale(domain=[870000000000, 1280000000000])),
                y=alt.Y('Montant de prime:Q', scale=alt.Scale(domain=[240, 266]))
            )
        else:
            line_prime = alt.Chart(dataframe_evol_primes).mark_line(strokeWidth=6, color='darkred').encode(
                x=alt.X('Annee:T', scale=alt.Scale(domain=[870000000000, 1280000000000])),
                y=alt.Y('Montant de prime:Q', scale=alt.Scale(domain=[150, 300]))
            )

        # Transparent selectors across the chart. This is what tells us the x-value of the cursor
        selectors_prime = alt.Chart(dataframe_evol_primes).mark_point().encode(
            x='Annee:T',
            opacity=alt.value(0),
        ).add_selection(
            nearest_prime
        )

        # Draw points on the line, and highlight based on selection
        points_prime = line_prime.mark_point().encode(
            opacity=alt.condition(nearest_prime, alt.value(1), alt.value(0))
        )

        # Draw text labels near the points, and highlight based on selection
        text_prime = line_prime.mark_text(color='darkgrey', align='left', dx=-25, dy=20, size=20,
                                          fontWeight="bold").encode(
            text=alt.condition(nearest_prime, 'Montant de prime:Q', alt.value(' '), format=".1f")
        )
        # Draw a rule at the location of the selection
        rules_prime = alt.Chart(dataframe_evol_primes).mark_rule(color='gray').encode(
            x='Annee:T',
        ).transform_filter(
            nearest_prime
        )

        # Put the five layers into a chart and bind the data
        graphe_prime = alt.layer(
            line_prime,
            selectors_prime,
            points_prime,
            text_prime,
            rules_prime
        )

        st.write("On dispose de données relatives au montant de primes acquises entre 1998 et 2010 par une compagnie d'assurance (en millions d'euros).")
        st.write("Selon vous, à combien s'élève le montant de primes acquises l'année suivante (2011) ? 5 ans plus tard (2015) ?")

        # st.altair_chart(line_prime,True)
        st.altair_chart(graphe_prime, True)

        if st.session_state.alea2 < 0.5:
            with st.form(key="montant_prime"):
                slider_prime_un_an = st.slider("Montant de primes en 2011 ?", 200.0, 350.0, 240.0)
                slider_prime_cinq_ans = st.slider("Montant de primes en 2015 ?", 200.0, 350.0, 240.0)
                sb_montant_prime = st.form_submit_button(label="Page suivante")

        else:
            with st.form(key="montant_prime"):
                slider_prime_un_an = st.slider("Montant de primes en 2011 ?", 200.0, 350.0, 300.0)
                slider_prime_cinq_ans = st.slider("Montant de primes en 2015 ?", 200.0, 350.0, 300.0)
                sb_montant_prime = st.form_submit_button(label="Page suivante")

        if sb_montant_prime:
            st.session_state.page += 1
            st.session_state.user_data.append("Montant de prime à un an")
            st.session_state.user_data.append(slider_prime_un_an)
            st.session_state.user_data.append("Montant de prime à cing an")
            st.session_state.user_data.append(slider_prime_cinq_ans)

            # GROUPE QUESTION SUIVANTE
            st.session_state.alea = random.uniform(0, 1)
            st.session_state.user_data.append(st.session_state.alea)
            if st.session_state.alea < 0.5:
                st.session_state.user_data.append("Moyenne basse")
            else:
                st.session_state.user_data.append("Moyenne haute")
            # GROUPE QUESTION SUIVANTE

            st.experimental_rerun()

    # Evolution de la charge sinistre (retour moyenne)
    elif st.session_state.page == 4:

        Year = [2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016]
        Moyenne_bas = [74.797696, 82.036351, 76.343512, 78.146366, 74.180035, 81.828443, 81.356627, 86.071678, 72.779008, 76.031071, 72.709526, 70.671256, 79.007412, 77.816575, 55.438527]
        Moyenne_haut = [74.797696, 82.036351, 76.343512, 78.146366, 74.180035, 81.828443, 81.356627, 86.071678, 72.779008, 76.031071, 72.709526, 70.671256, 79.007412, 77.816575, 108.242495]

        data_bas = {"annee": Year, "charge": Moyenne_bas}
        dataframe_bas = pd.DataFrame(data_bas)

        data_haut = {"annee": Year, "charge": Moyenne_haut}
        dataframe_haut = pd.DataFrame(data_haut)

        # Create a selection that chooses the nearest point & selects based on x-value
        nearest = alt.selection(type='single', nearest=True, on='mouseover',
                                fields=['annee'], empty='none')

        if st.session_state.alea < 0.5:

            # The basic line
            line_bas_rouge = alt.Chart(dataframe_bas).mark_line(strokeWidth=5, color='crimson').encode(
                x=alt.X('annee:T', scale=alt.Scale(domain=[982000000000, 1470000000000])),
                y=alt.Y('charge:Q', scale=alt.Scale(domain=[50, 90]))
            )

            # Transparent selectors across the chart. This is what tells us the x-value of the cursor
            selectors = alt.Chart(dataframe_bas).mark_point().encode(x='annee:T', opacity=alt.value(0),).add_selection(nearest)

            # Draw points on the line, and highlight based on selection
            points_bas_rouge = line_bas_rouge.mark_point().encode(opacity=alt.condition(nearest, alt.value(1), alt.value(0)))

            # Draw text labels near the points, and highlight based on selection
            text_bas_rouge = line_bas_rouge.mark_text(color='darkgrey', align='left', dx=-25, dy=20, size=20, fontWeight="bold").encode(text=alt.condition(nearest, 'charge:Q', alt.value(' '), format=".1f"))

            # Draw a rule at the location of the selection
            rules = alt.Chart(dataframe_bas).mark_rule(color='gray').encode(x='annee:T',).transform_filter(nearest)

            # Put the five layers into a chart and bind the data
            graphe_bas_rouge = alt.layer(line_bas_rouge, selectors, points_bas_rouge, text_bas_rouge, rules)

            st.write("On dispose des données relatives à la charge de sinistre de la LoB MRH d'une compagnie d'assurance entre 2002 et 2017 (en millions d'euros).")
            st.markdown("Aucune évolution notable n'est à relever pour ce qui est du profil de risque du portefeuille.")

            col1, col2 = st.columns(2)
            with col1:
                st.altair_chart(graphe_bas_rouge, True)

            with col2:
                st.write(dataframe_bas)

            st.write("A votre avis, à combien devrait s'élèver la charge de sinistre pour l'année 2018 ? Et pour l'année 2022 (en millions)")

            with st.form(key="retour_moyenne_1"):
                slider_retour_moyenne = st.slider("Charge sinistre en 2018 ? ", 0.0, 110.0, 55.0)
                slider_retour_moyenne_2 = st.slider("Charge sinistre en 2022 ? ", 0.0, 110.0, 55.0)
                sb_retour_moyenne = st.form_submit_button(label="Page suivante")

        else:

            # The basic line
            line_haut_vert = alt.Chart(dataframe_haut).mark_line(strokeWidth=5, color='mediumseagreen').encode(x=alt.X('annee:T', scale=alt.Scale(domain=[982000000000, 1470000000000])), y=alt.Y('charge:Q', scale=alt.Scale(domain=[65, 115])))

            # Transparent selectors across the chart. This is what tells us the x-value of the cursor
            selectors = alt.Chart(dataframe_haut).mark_point().encode(x='annee:T', opacity=alt.value(0),).add_selection(nearest)

            # Draw points on the line, and highlight based on selection
            points_haut_vert = line_haut_vert.mark_point().encode(opacity=alt.condition(nearest, alt.value(1), alt.value(0)))

            # Draw text labels near the points, and highlight based on selection
            text_haut_vert = line_haut_vert.mark_text(color='darkgrey', align='left', dx=-25, dy=35, size=20, fontWeight="bold").encode(text=alt.condition(nearest, 'charge:Q', alt.value(' '), format=".1f"))

            # Draw a rule at the location of the selection
            rules = alt.Chart(dataframe_haut).mark_rule(color='gray').encode(x='annee:T',).transform_filter(nearest)

            # Put the five layers into a chart and bind the data
            graphe_haut_vert = alt.layer(line_haut_vert, selectors, points_haut_vert, rules, text_haut_vert)

            st.write("On dispose des données relatives à la charge de sinistre de la LoB auto d'une compagnie d'assurance entre 2002 et 2017 (en millions d'euros).")
            st.markdown("Aucune évolution notable n'est à relever pour ce qui est du profil de risque du portefeuille.")

            col1, col2 = st.columns(2)
            with col1:
                st.altair_chart(graphe_haut_vert, True)

            with col2:
                st.write(dataframe_haut)

            st.write("Selon vous, à combien devrait s'élever la charge de sinistre pour l'année 2018 ? Et pour l'année 2022 (en millions)")

            with st.form(key="retour_moyenne_1"):
                slider_retour_moyenne = st.slider("Charge sinistre en 2018", 60.0, 160.0, 110.0)
                slider_retour_moyenne_2 = st.slider("Charge sinistre en 2022 ? ", 0.0, 220.0, 110.0)
                sb_retour_moyenne = st.form_submit_button(label="Page suivante")

        if sb_retour_moyenne:
            st.session_state.user_data.append("Valeur retour moyenne")
            st.session_state.user_data.append(slider_retour_moyenne)
            st.session_state.user_data.append(slider_retour_moyenne_2)
            st.session_state.page += 1
            st.experimental_rerun()

    # Gambler's fallacy
    elif st.session_state.page == 5:

        st.header("Approche du risque")

        with st.form(key="gambler"):
            st.write("La probabilité moyenne d'avoir un accident non-responsable pour les individus en portefeuille est estimée à 2%. Les assurés A et B ont le même profil de risque et les mêmes pratiques de conduite. ")
            st.write("L’année dernière, l’individu A a eu 4 accidents auto non responsables tandis que B n'en a pas eu.")
            accident = st.text_input("Qui est le plus susceptible d'avoir un nouvel accident le premier ?")
            sb_gambler = st.form_submit_button(label="Page suivante")

        if sb_gambler:
            st.session_state.page += 1
            st.session_state.user_data.append("Individu accident")
            st.session_state.user_data.append(accident)

            # GROUPE QUESTION SUIVANTE
            st.session_state.alea = random.uniform(0, 1)
            st.session_state.user_data.append(st.session_state.alea)
            if st.session_state.alea < 0.5:
                st.session_state.user_data.append("Ancre : 62%")
            else:
                st.session_state.user_data.append("Ancre : 124%")
            # GROUPE QUESTION SUIVANTE

            st.experimental_rerun()

    # Position par rapport à l'ancre MRH
    elif st.session_state.page == 6:

        st.header("Marché assurantiel")

        if st.session_state.alea < 0.5:
            with st.form(key="marche_MRH"):
                st.write("Selon vous, le ratio combiné du secteur de l'assurance multirisque habitation en France en 2020 était-il supérieur ou inférieur à 62% ?")
                ancre_MRH = st.selectbox(" ", ["-", "Supérieur", "Inférieur"])
                sb_position_ancre = st.form_submit_button(label="Page suivante")

        else:

            with st.form(key="marche_MRH"):
                st.write("Selon vous, le ratio combiné du secteur de l'assurance multirisque habitation en France en 2020 était-il supérieur ou inférieur à 124% ?")
                ancre_MRH = st.selectbox(" ", ["-", "Supérieur", "Inférieur"])
                sb_position_ancre = st.form_submit_button(label="Page suivante")

        if sb_position_ancre:

            st.session_state.page += 1
            st.session_state.user_data.append("Position vis à vis de l'ancre")
            st.session_state.user_data.append(ancre_MRH)

            st.experimental_rerun()

    # Ratio S/P MRH
    elif st.session_state.page == 7:

        st.header("Marché assurantiel")

        if st.session_state.alea < 0.5:

            with st.form(key="marche_MRH"):
                st.write("A combien estimeriez-vous ce ratio combiné ?")
                marche_MRH = st.slider("Ratio combiné MRH (2020)", min_value=20, max_value=160, value=62)
                sb_ancre_MRH = st.form_submit_button(label="Page suivante")

        else:

            with st.form(key="marche_MRH"):
                st.write("A combien estimeriez-vous ce ratio combiné ?")
                marche_MRH = st.slider("Ratio combiné MRH (2020)", min_value=20, max_value=160, value=124)
                sb_ancre_MRH = st.form_submit_button(label="Page suivante")

        if sb_ancre_MRH:

            st.session_state.page += 1

            st.session_state.user_data.append("Ratio combiné MRH en 2020")
            st.session_state.user_data.append(marche_MRH)

            st.session_state.alea = random.uniform(0, 1)
            st.session_state.user_data.append(st.session_state.alea)
            if st.session_state.alea < 0.5:
                st.session_state.user_data.append("Comparaison auto - terrorisme")
            else:
                st.session_state.user_data.append("Comparaison auto - ")

            st.experimental_rerun()

    # Intervalle de confiance S/P auto
    elif st.session_state.page == 800:

        st.header("Marché assurantiel")

        with st.form(key="marche_auto"):
            st.write("Donnez un intervalle pour le ratio S/P du secteur automobile français en 2019 avec une certitude de 90%")
            marche_auto = st.slider("Ratio S/P du secteur automobile français", min_value=50, max_value=150, value=(90, 110))
            sb_SP_marche_auto = st.form_submit_button(label="Page suivante")

        if sb_SP_marche_auto:

            st.session_state.page += 1
            st.session_state.user_data.append("Ratio S/P du marché automobile en 2020")
            st.session_state.user_data.extend(marche_auto)

            st.experimental_rerun()

    # Biais de disponibilité
    elif st.session_state.page == 801:

        st.header("Marché assurantiel")

        with st.form(key="charge_sinistre"):
            st.write("Selon vous ")
            st.write("Quel est, selon vous, le nombre d'hôpitaux français visés par une cyberattaque en 2020 ?")
            st.write("2 : Quel est, selon vous, le nombre  ?")
            attaque_hopitaux = st.text_input(label="Nombre d'hôpitaux visés par une cyberattque")
            sb_biais_cognitifs = st.form_submit_button(label="Page suivante")

        if sb_biais_cognitifs:

            st.session_state.page += 1
            st.session_state.user_data.append("Attaque hopitaux")
            st.session_state.user_data.extend(attaque_hopitaux)

            # GROUPE QUESTION SUIVANTE
            st.session_state.alea = random.uniform(0, 1)
            st.session_state.user_data.append(st.session_state.alea)
            if st.session_state.alea < 0.5:
                st.session_state.user_data.append("Framing positif")
            else:
                st.session_state.user_data.append("Framing négatif")
            # GROUPE QUESTION SUIVANTE

            st.experimental_rerun()

    # Maladie Kahneman
    elif st.session_state.page == 8:

        st.header("Attitude face au risque")

        if st.session_state.alea < 0.5:
            with st.form(key="test_framing_kahneman"):
                st.write("La France s'attend à l'arrivée d'une maladie infectieuse, supposée tuer 600 personnes. Deux programmes de traitement sont disponibles pour endiguer la maladie :")
                st.write("- Si le programme A est adopté, 200 personnes seront sauvées")
                st.write("- Si le programme B est adopté, il y a 1/3 de chances que 600 personnes soient sauvées et 2/3 de chances que personne ne soit sauvé")
                programme = st.selectbox("Quel programme vous semble préférable ?", ["-", "Programme A", "Programme B"])
                sb_framing_kahneman = st.form_submit_button(label="Page suivante")

        else:
            with st.form(key="test_framing_kahneman"):
                st.write("La France s'attend à l'arrivée d'une maladie infectieuse, supposée tuer 600 personnes. Deux programmes de traitement sont disponibles pour endiguer la maladie :")
                st.write("- Si le programme A est adopté, 400 personnes mourront")
                st.write("- Si le programme B est adopté, il y a 1/3 de chances que personne ne meure et 2/3 de chances que 600 personnes meurent")
                programme = st.selectbox("Quel programme vous semble préférable ?", ["-", "Programme A", "Programme B"])
                sb_framing_kahneman = st.form_submit_button(label="Page suivante")

        if sb_framing_kahneman:
            st.session_state.page += 1
            st.session_state.user_data.append(programme)
            st.experimental_rerun()

    # Remarques
    elif st.session_state.page == 9:

        with st.form(key='my_form_end'):
            retour_utilisateur = st.text_input(label='Vous pouvez noter ici des remarques éventuelles')
            submit_button_end = st.form_submit_button(label="Terminer l'étude et envoyer les résultats")

        if submit_button_end:

            st.session_state.user_data.append(retour_utilisateur)

            from datetime import datetime
            from datetime import date
            end = datetime.now()
            temps_fin = end.strftime("%H:%M:%S")
            st.session_state.user_data.append(temps_fin)

            import gspread

            credentials = {
                "type": st.secrets["s_type"],
                "project_id": st.secrets["s_project_id"],
                "private_key_id": st.secrets["s_private_key_id"],
                "private_key": st.secrets["s_private_key"],
                "client_email": st.secrets["s_client_email"],
                "client_id": st.secrets["s_client_id"],
                "auth_uri": st.secrets["s_auth_uri"],
                "token_uri": st.secrets["s_token_uri"],
                "auth_provider_x509_cert_url": st.secrets["s_auth_provider_x509_cert_url"],
                "client_x509_cert_url": st.secrets["s_client_x509_cert_url"]
            }

            gc = gspread.service_account_from_dict(credentials)
            sh = gc.open("Resultats_questionnaire")
            worksheet = sh.sheet1
            worksheet.insert_row(st.session_state.user_data, 1)

            st.session_state.page = 999
            st.experimental_rerun()

    # Page de fin
    elif st.session_state.page == 999:

        st.write("Vos résultats ont bien été pris en compte.")
        st.write("Merci pour votre participation !")
        st.markdown("Pour toute remarque ou commentaire complémentaire, n'hésitez pas à contacter Romain Chabert à l'adresse <a href='mailto:rchabert@deloitte.fr'>rchabert@deloitte.fr</a>.", unsafe_allow_html=True)

        retour_menu = st.button("Retourner au menu")

        if retour_menu:
            st.session_state.menu = 0
            st.experimental_rerun()

    # my_bar.empty()

elif st.session_state.menu == 2:

    st.session_state.retour_menu_CP = False

    # http://metadataconsulting.blogspot.com/2019/03/OneDrive-2019-Direct-File-Download-URL-Maker.html

    st.write("Cette seconde partie de l'étude, à effectuer sur un tableur, est constituée d'une série de cas pratiques sous Excel. [Appuyez sur ce lien] (https://onedrive.live.com/download?cid=E1CA44655646A7B5&resid=E1CA44655646A7B5%21261243&authkey=AIYTfMbO53hkK5o&em=2) pour télécharger le fichier Excel.")
    st.write("_Attention : bien penser à enregistrer le fichier téléchargé avant de pouvoir le renvoyer ensuite._")

    st.markdown("Une fois terminé, merci de retourner le cas pratique par mail à l'adresse suivante : <a href='mailto:rchabert@deloitte.fr'>rchabert@deloitte.fr</a>.", unsafe_allow_html=True)

    st.write("Merci pour votre participation !")

    st.session_state.retour_menu_CP = st.button("Retour")

    if st.session_state.retour_menu_CP:
        st.session_state.menu = 0
        st.experimental_rerun()
