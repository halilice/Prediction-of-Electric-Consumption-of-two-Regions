import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

def prediction_energy():
    col1, col2, col3 = st.columns([1, 2, 1], gap="small")
    with col2:
        st.markdown("<h1 style='text-align: center;'>Application de la Prédiction de la Consommation d'Electricité</h1>",
                    unsafe_allow_html=True)

        st.text("""
            Bienvenue sur l'application de prévision de la consommation électrique des régions 
            Centre-val-de-Loire et Hauts-de-France. L'application va prédire la consommation 
            électrique journalière avec les informations que vous allez entrer. Nous vous demanderons 
            quelques informations sur la météo du jour. Vous pouvez trouver toutes les informations 
            nécessaires concernant la météo sur le site << https://www.yr.no/en >>. 
            """)

        df = pd.read_csv('matrice_ml_enedis.csv')
        df['Energy_Cons_KWh'] = df['Energy_Cons_KWh'].apply(lambda x: x / 1000)
        df.rename({'Energy_Cons_KWh': 'Energy_Cons_mWh'}, axis=1, inplace=True)


        X = df[['Région', 'Jour_Feries', 'Vacances_Scol', 'TOTAL_SNOW_MM', 'MAX_TEMPERATURE_C', 
                'HUMIDITY_MAX_PERCENT', 'PRECIP_TOTAL_DAY_MM', 'SUNHOUR']]
        y = df['Energy_Cons_mWh']

        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, train_size=0.75)

        numeric=['MAX_TEMPERATURE_C', 'HUMIDITY_MAX_PERCENT', 'PRECIP_TOTAL_DAY_MM', 'SUNHOUR']

        sc=StandardScaler()
        X_train[numeric]=sc.fit_transform(X_train[numeric])
        X_test[numeric]=sc.transform(X_test[numeric])

        rf = RandomForestRegressor().fit(X_train, y_train)
        rf_pred = rf.predict(X_test)


        region = st.selectbox("Veuillez choisir la région pour laquelle vous souhaitez que nous fassions des prédictions", 
                              options = ['Centre-val-de-Loire', 'Hauts-de-France'])

        nat_hol = st.radio("Le jour que vous voulez nous faire prédire est-il un jour férié ?", ['Oui', 'Non'])

        school_hol = st.radio("Le jour que vous voulez que nous prédisions est-il celui des vacances scolaires ?", ['Oui', 'Non'])

        snow = st.radio("Le jour est-il neigeux ?", ['Oui', 'Non'])

        temperature = st.number_input("Veuillez indiquer la température maximale de la journée en C°", 
                                      min_value=None, max_value=None, placeholder="Saisir un chiffre...")
        humidity = st.number_input("Veuillez saisir le pourcentage d'humidité de la journée", 
                                   min_value=None, max_value=None, placeholder="Saisir un chiffre...")

        precipitation = st.number_input("Veuillez indiquer le total des précipitations de la journée en mm.", 
                                        min_value=None, max_value=None, placeholder="Saisir un chiffre...")

        sunhour = st.number_input("Veuillez saisir l'heure du soleil de la journée", 
                                        min_value=None, max_value=None, placeholder="Saisir un chiffre...")

        input_values = []
        if region == 'Centre-val-de-Loire':
            input_values.append(1)
        else:
            input_values.append(2)

        list_radio = [nat_hol, school_hol, snow]
        for i in range(len(list_radio)):
            if list_radio[i] == 'Yes':
                input_values.append(1)
            else:
                input_values.append(0)

        input_values.append(temperature)
        input_values.append(humidity)
        input_values.append(precipitation)
        input_values.append(sunhour)

        vaar_scale = input_values[4:8]
        vaar_scaled = sc.transform([vaar_scale])

        vaar_scaled = vaar_scaled.ravel().tolist()

        #st.write(vaar_scaled)

        input_values = input_values[0:4] + vaar_scaled

        #st.write(input_values)


        ypred = rf.predict([input_values])

        st.write(f"La consommation électrique de la journée avec les informations que vous avez saisies est de {ypred.round(2)} mWh") 
        
        if region == 'Centre-val-de-Loire':
            region = 1
        else:
            region = 2
        filter1 = df['MAX_TEMPERATURE_C'] <= temperature + 3
        filter2 = df['MAX_TEMPERATURE_C'] >= temperature - 3
        filter3 = df['Région'] == region
        new_df = df[filter1 & filter2 & filter3]
        
        lower = int(ypred) - 5000
        upper = int(ypred) + 5000
        
        st.markdown('#')
        
        st.subheader("Comparaison des Prédictions avec les Données Réelles")
        if region == 1:
            fig = px.box(
                new_df,
                x='Région',
                y='Energy_Cons_mWh'
            )

            fig.update_layout(
                yaxis_title="Consommation électrique totale (mWh)",
                xaxis_title="Région: Centre-val-de-Loire",
                margin=dict(l=20, r=20, t=100, b=30),
                yaxis_range=[int(lower), int(upper)]
            )
            fig.add_trace(go.Scatter(x=[1], y=[int(ypred)], mode = 'markers',
                             marker_symbol = 'star', marker_color = 'red',
                             marker_size = 30))
            fig.update_xaxes(showticklabels=False)
            st.plotly_chart(fig)

        else:
            fig = px.box(
                new_df,
                x='Région',
                y='Energy_Cons_mWh'
            )

            fig.update_layout(
                yaxis_title="Consommation électrique totale (mWh)",
                xaxis_title="Région: Hauts-de-France",
                margin=dict(l=20, r=20, t=100, b=30),
                yaxis_range=[int(lower), int(upper)]
            )
            fig.add_trace(go.Scatter(x=[2], y=[int(ypred)], mode = 'markers',
                             marker_symbol = 'star', marker_color = 'red',
                             marker_size = 30))
            fig.update_xaxes(showticklabels=False)

            st.plotly_chart(fig)





