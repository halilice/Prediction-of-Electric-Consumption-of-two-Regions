import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Execute the following code to avoid displaying the numbers in scientific notation
pd.options.display.float_format = '{:.2f}'.format

# Execute the following code to avoid the 'SettingWithCopyWarning' warnings
pd.options.mode.chained_assignment = None

# Execute the following code to avoid the 'FutureWarning'
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


def basic_indicators():    
    st.markdown("<h1 style='text-align: center;'>INDICATEURS CLÉS</h1>", unsafe_allow_html=True)

    #st.markdown('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)

    st.markdown('#')


    df_new = pd.read_csv('csv_files/df_new.csv')

    df_cons_hour = pd.read_csv('csv_files/df_cons_hour.csv')

    df_cons_prof = pd.read_csv('csv_files/df_cons_prof.csv')

    enr_sub_pow_range = pd.read_csv('csv_files/enr_sub_pow_range.csv')


    col1, col2 = st.columns(2, gap="small")

    with col1:
        # PLot the graph
        st.subheader("Consommation d'Electricité par Région au Fil du Temps")
        fig = px.line(
            df_new,
            x="Date",
            y="Total énergie soutirée (Wh)",
            color="Région",
            # title="Energy Consumption by Regions over Time",
            height=600,
            color_discrete_sequence=['#FF7F0E', '#1F77B4']
        )

        fig.update_layout(
            yaxis_title="Consommation électrique totale (mWh)",
            margin=dict(l=20, r=20, t=100, b=30),
            yaxis_range=[0,80000]
        )
        fig.update_xaxes(tickangle=315)

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader('Consommation Electrique par Région par 1/2 Heure')
        # Average energy consumption by 1/2 hour
        fig = px.line(
            df_cons_hour,
            x="hour",
            y="Total énergie soutirée (Wh)",
            # title="Energy Consumption by Regions per 1/2 hour",
            height=600
        )

        fig.update_layout(
            yaxis_title="Consommation électrique totale (mWh)",
            xaxis_title="Heure",
            margin_pad=20,
            margin=dict(l=20, r=20, t=100, b=30),
            yaxis_range=[0,1500]
        )
        fig.update_xaxes(tickangle=315)

        fig.update_traces(line=dict(color="Red", width=5))

        st.plotly_chart(fig, use_container_width=True)

    st.markdown('#')

    col3, col4 = st.columns(2, gap="small")

    with col3:
        st.subheader("Consommation Electrique Moyenne par Profil d'Abonnement")
        # Energy consumption by subscription profile & region
        fig = px.histogram(
            df_cons_prof,
            x="Profil",
            y="Total énergie soutirée (Wh)",
            barmode="group",
            # title="Energy Consumption by Regions per 1/2 hour",
            color="Région",
            height=650,
            color_discrete_sequence=px.colors.qualitative.D3
        )

        fig.update_layout(
            yaxis_title="Consommation électrique totale (mWh)",
            xaxis_title="Profil",
            margin_pad=20,
            margin=dict(l=20, r=20, t=20, b=20)
        )
        fig.update_xaxes(tickangle=315)

        st.plotly_chart(fig, use_container_width=True)

    with col4:
        st.subheader('Consommation Electrique Moyenne par Plage de Puissance Souscrite et par Région en Pourcentage')
        tot_energy_cons=pd.read_csv('csv_files/tot_energy_cons.csv')
        tot_energy_cons = tot_energy_cons[tot_energy_cons['Plage de puissance souscrite'] != 'P0: Total <= 36 kVA']

        list_profiles = tot_energy_cons['Profil'].unique().tolist()
        list_profiles.insert(0, 'Tous les Profils')
        profile = st.selectbox('Sélectionner le profil', list_profiles)

        if profile == 'Tous les Profils':
            new_df = tot_energy_cons.copy()
        else:
            new_df = tot_energy_cons[tot_energy_cons['Profil'] == profile]

        new = new_df.groupby(by = ['Plage de puissance souscrite', 'Région'], as_index=False)[['total_enr_cons']].sum()

        new['percentage'] = 100 * new['total_enr_cons'] / new.groupby(by='Région', as_index=False)['total_enr_cons'].transform('sum')
        new = new.sort_values(by='total_enr_cons')

        fig = px.histogram(
                new,
                x="percentage",
                y="Plage de puissance souscrite",
                color="Région",
                barmode="group",
                height=500,
                color_discrete_sequence=px.colors.qualitative.D3
        )

        fig.update_layout(
                yaxis_title="Plage de puissance souscrite",
                xaxis_title="Pourcentage",
                margin=dict(l=20, r=20, t=20, b=20)
        )

        st.plotly_chart(fig, use_container_width=True)


    
    
def indicators_matrix():
    
    st.markdown("<h1 style='text-align: center;'>INDICATEURS DE LA MATRICE DU MODÈLE ML</h1>", unsafe_allow_html=True)
    
    df_matrix = pd.read_csv('csv_files/matrice_ml_enedis.csv')
    
    df_matrix['Energy_Cons_KWh'] = df_matrix['Energy_Cons_KWh'].apply(lambda x: x / 1000)
    
    dico_regions = {1: 'Centre-Val de Loire', 2: 'Hauts-de-France'}
    df_matrix['Région'] = df_matrix['Région'].replace(dico_regions)
    
    dico_seasons = {'Winter': 'Hiver', 'Spring': 'Printemps', 'Summer': 'Eté', 'Fall': 'Automne'}
    df_matrix['season'] = df_matrix['season'].replace(dico_seasons)
    
    st.markdown('#')

    list_regions = df_matrix['Région'].unique().tolist()
    list_regions.insert(0, 'Toutes les régions')
    regions = st.sidebar.radio('Sélectionnez la région', list_regions)

    if regions == 'Toutes les régions':
        new_df_matrix = df_matrix.copy()
    else:
        new_df_matrix = df_matrix[df_matrix['Région'] == regions]

    list_seasons = df_matrix['season'].unique().tolist()
    list_seasons.insert(0, 'Toutes les saisons')
    seasons = st.sidebar.radio('Sélectionner la saison', list_seasons)

    if seasons == 'Toutes les saisons':
        new_df_matrix = df_matrix.copy()
    else:
        new_df_matrix = df_matrix[df_matrix['season'] == seasons]
            
    if regions=='Toutes les régions' and seasons=='Toutes les saisons':
        new_df_matrix = df_matrix.copy()
    elif regions != 'Toutes les régions' and seasons=='Toutes les saisons':
        new_df_matrix = df_matrix[df_matrix['Région'] == regions]
    elif seasons != 'Toutes les saisons' and regions=='Toutes les régions':
        new_df_matrix = df_matrix[df_matrix['season'] == seasons]
    elif regions != 'Toutes les régions' and seasons != 'Toutes les saisons':
        new_df_matrix = df_matrix[ (df_matrix['Région'] == regions) & (df_matrix['season'] == seasons)]
    
    col1, col2 = st.columns(2, gap="small")

    with col1:
        st.subheader('Consommation Electrique par Température Maximale')
        fig = px.scatter(
                new_df_matrix,
                x="MAX_TEMPERATURE_C",
                y="Energy_Cons_KWh",
                color="season",
                height=500,
                color_discrete_sequence=px.colors.qualitative.D3
        )

        fig.update_layout(
                yaxis_title="Consommation électrique totale (mWh)",
                xaxis_title="Max Température C°",
                margin=dict(l=20, r=20, t=20, b=20)
        )

        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        new_df_matrix['PRECIP_TOTAL_DAY_MM'] = new_df_matrix['PRECIP_TOTAL_DAY_MM'].apply(lambda x: 'Pluvieux' if x != 0 
                                                                                          else 'Non Pluvieux')
        st.subheader("Consommation d'Electricité par Précipitation Total")
        fig = px.box(
                new_df_matrix,
                x="PRECIP_TOTAL_DAY_MM",
                y="Energy_Cons_KWh",
                height=500,
                color_discrete_sequence=px.colors.qualitative.D3
        )

        fig.update_layout(
                yaxis_title="Consommation électrique totale (mWh)",
                xaxis_title="Précipitation Total MM",
                margin=dict(l=20, r=20, t=20, b=20)
        )

        st.plotly_chart(fig, use_container_width=True)
    
    
    st.markdown('#')
    
    col3, col4 = st.columns(2, gap="small")

    with col3:
        
        avg_energy_cons = new_df_matrix.groupby('Région').\
                        agg(**{'Average_enrgy_cons': ('Energy_Cons_KWh', lambda x: x.mean())}).\
                        reset_index()
        avg_energy_cons['Average_enrgy_cons'] = avg_energy_cons['Average_enrgy_cons'].apply(lambda x: round(x, 0))
        st.subheader('Consommation Electrique par Région')
        fig = px.bar(
                avg_energy_cons,
                x="Région",
                y="Average_enrgy_cons",
                color="Région",
                height=400,
                color_discrete_sequence=['#FF7F0E', '#1F77B4'],
                text_auto='.0f'
        )

        fig.update_layout(
                barcornerradius=15,
                yaxis_title="Consommation électrique totale (mWh)",
                xaxis_title="Région",
                margin=dict(l=20, r=20, t=20, b=20)
        )

        st.plotly_chart(fig, use_container_width=True)
        
    with col4:
        st.subheader('Consommation Electrique par Heure de Soleil')
        fig = px.scatter(
                new_df_matrix,
                x="SUNHOUR",
                y="Energy_Cons_KWh",
                color="Région",
                height=400,
                color_discrete_sequence=['#FF7F0E', '#1F77B4']
        )

        fig.update_layout(
                    barcornerradius=15,
                    yaxis_title="Consommation électrique totale (mWh)",
                    xaxis_title="Heure de Soleil",
                    margin=dict(l=20, r=20, t=20, b=20)
        )


        st.plotly_chart(fig, use_container_width=True)
        
        
    st.markdown('#')

    
    col5, col6 = st.columns(2, gap="small")
        
    with col5:
        st.subheader("Consommation Electrique en Fonction de l'Humidité")
        humidity = new_df_matrix.groupby(['HUMIDITY_MAX_PERCENT', 'Région']).\
                        agg(**{'Average_enrgy_cons': ('Energy_Cons_KWh', lambda x: x.mean())}).\
                        reset_index()
        fig = px.scatter(
                new_df_matrix,
                x="HUMIDITY_MAX_PERCENT",
                y="Energy_Cons_KWh",
                color="Région",
                height=400,
                color_discrete_sequence=['#FF7F0E', '#1F77B4']
        )

        fig.update_layout(
                    barcornerradius=15,
                    yaxis_title="Consommation électrique totale (mWh)",
                    xaxis_title="Humidité (Pourcentage)",
                    margin=dict(l=20, r=20, t=20, b=20)
        )


        st.plotly_chart(fig, use_container_width=True)
        
    with col6:
        dico_snowy = {0: 'Pas Neigeux', 1: 'Neigeux'}
        new_df_matrix['TOTAL_SNOW_MM'] = new_df_matrix['TOTAL_SNOW_MM'].replace(dico_snowy)
        st.subheader("Consommation d'Electricité par la Neige")
        fig = px.box(
                new_df_matrix,
                x="TOTAL_SNOW_MM",
                y="Energy_Cons_KWh",
                color="Région",
                height=400,
                color_discrete_sequence=['#FF7F0E', '#1F77B4']
        )

        fig.update_layout(
                barcornerradius=15,
                yaxis_title="Consommation électrique totale (mWh)",
                xaxis_title="Neige",
                margin=dict(l=20, r=20, t=20, b=20)
        )
        

        st.plotly_chart(fig, use_container_width=True)
        
        
    st.markdown('#')
    
    col7, col8, col9 = st.columns([1,2,1], gap="small")
    with col8:
        st.subheader("Consommation d'Electricité par Jour de Vacances")
        cols = ['Jour_Feries', 'Weekend', 'Vacances_Scol']
        calendrier = st.selectbox('Sélectionner le calendrier', cols)
        if calendrier == 'Jour_Feries':
            dico_feries = {0: 'Journée Normale', 1: 'Jour_Feries'}
            new_df_matrix['Jour_Feries'] = new_df_matrix['Jour_Feries'].replace(dico_feries)
            feries = new_df_matrix.groupby(['Jour_Feries', 'Région']).\
                        agg(**{'Average_enrgy_cons': ('Energy_Cons_KWh', lambda x: x.mean())}).\
                        reset_index()
            fig = px.bar(
                feries,
                x="Jour_Feries",
                y="Average_enrgy_cons",
                color="Région",
                barmode='group',
                height=400,
                color_discrete_sequence=['#FF7F0E', '#1F77B4'],
                text_auto='.0f'
            )

            fig.update_layout(
                    barcornerradius=15,
                    yaxis_title="Consommation électrique totale (mWh)",
                    xaxis_title="Jour férié",
                    margin=dict(l=20, r=20, t=20, b=20)
            )

            st.plotly_chart(fig, use_container_width=True)
            
        elif calendrier == 'Weekend':
            dico_weekend = {0: 'Pas Week-end', 1: 'Week-end'}
            new_df_matrix['Weekend'] = new_df_matrix['Weekend'].replace(dico_weekend)
            weekend = new_df_matrix.groupby(['Weekend', 'Région']).\
                        agg(**{'Average_enrgy_cons': ('Energy_Cons_KWh', lambda x: x.mean())}).\
                        reset_index()
            fig = px.bar(
                weekend,
                x="Weekend",
                y="Average_enrgy_cons",
                color="Région",
                barmode='group',
                height=400,
                color_discrete_sequence=['#FF7F0E', '#1F77B4'],
                text_auto='.0f'
            )

            fig.update_layout(
                    barcornerradius=15,
                    yaxis_title="Consommation électrique totale (mWh)",
                    xaxis_title="Week-end",
                    margin=dict(l=20, r=20, t=20, b=20)
            )

            st.plotly_chart(fig, use_container_width=True)
            
            
        else:
            dico_school = {0: 'Journée Normale', 1: 'Vacances_Scol'}
            new_df_matrix['Vacances_Scol'] = new_df_matrix['Vacances_Scol'].replace(dico_school)
            school = new_df_matrix.groupby(['Vacances_Scol', 'Région']).\
                        agg(**{'Average_enrgy_cons': ('Energy_Cons_KWh', lambda x: x.mean())}).\
                        reset_index()
            fig = px.bar(
                school,
                x="Vacances_Scol",
                y="Average_enrgy_cons",
                color="Région",
                barmode='group',
                height=400,
                color_discrete_sequence=['#FF7F0E', '#1F77B4'],
                text_auto='.0f'
            )

            fig.update_layout(
                    barcornerradius=15,
                    yaxis_title="Consommation électrique totale (mWh)",
                    xaxis_title="Vacances scolaires",
                    margin=dict(l=20, r=20, t=20, b=20)
            )

            st.plotly_chart(fig, use_container_width=True)













