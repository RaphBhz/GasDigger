from asyncio.windows_events import NULL
import pandas as pd
import numpy as np
import datetime
import haversine as hs
import folium
import plotly.express as px

# Ceci est une fonction qui retourne
# Vrai : si la station se trouve à côté du client sur une distance qui est ici 'rayon'
# Faux : contraire

def calcul_distance(position_actuelle, station, rayon):   
    x = position_actuelle.split(",")
    y = station.split(",")
    
    loc1 = (float(x[0]),float(x[1]))
    loc2 = (float(y[0]),float(y[1]))
    distance = hs.haversine(loc1,loc2)
    if distance > rayon :
        return False
    if distance <= rayon :
        return True

######################################################################

def maps(df, carburant, prixmin, prixmax, maposition, list_services, rayon): 
    # Affichage pour voir le nombre de lignes
    print('Il y a ' + str(len(df)) + ' enregistrements dans les données avant de supprimer.')
    print()
    t1 = datetime.datetime.now()


    # Trier les données : Je pense à mettre toute cette étape dans une fonction ça sera plus simple
        # Le tri se fait sur cet ordre
        # type de carburant - prix - rayon de recherche - services

    df = df.query('prix_nom =="' + carburant + '" & prix_valeur < '+ str(prixmax) + '& prix_valeur > '+ str(prixmin))
    print(str(prixmax   ))

    # RAYON DE RECHERCHE
    for index, row in df.iterrows():
        if calcul_distance(maposition,row['geom'],rayon) == False: # On utilise la fonction calcul_distance
            df.drop(index, inplace=True)

    if list_services:
        for index, row in df.iterrows():
            if type(row['services_service']) == str:
                if not all(word in row['services_service'] for word in list_services):
                    df.drop(index, inplace=True)
            if type(row['services_service']) != str:
                df.drop(index, inplace=True)


    # Affichage des perf du programmes
    t2 = datetime.datetime.now()
    tm = round((t2 - t1).total_seconds(), 2)
    print('Il a fallu  ' + str(tm) + ' seconds pour suppprimer les données non-désirées.')
    print()
    print('Il y a ' + str(len(df)) + ' enregistrements dans les données après avoir supprimé ceux des pays non-désirées.')

    # L'utilisateur va choisir des options
    # 
    # ######################################

    # define the world map
    world_map = folium.Map()
    
    # create a Stamen Toner map of the world
    # centered around Mumbai

    x = maposition.split(",")
    mapos = [float(x[0]),float(x[1])]

    world_map = folium.Map(location =mapos, 
                        zoom_start = 9, tiles ='Stamen Toner')


    folium.Circle(mapos, rayon*1000, color="yellow",fill=True).add_child(folium.Popup('Rayon')).add_to(world_map)
    folium.Circle(
        location=mapos,
        radius=20,
        popup=mapos,
        color="#3186cc",
        fill=True,
        fill_color="#3186cc",
    ).add_to(world_map)


    for index, location_info in df.iterrows():
        gaspump = folium.Icon(color='black', icon='tint', icon_color="white", prefix='glyphicon')
        x = location_info["geom"].split(",")
        folium.Marker(
            [float(x[0]),float(x[1])], 
            popup=location_info["adresse"]+" "+location_info["ville"],
            icon=gaspump,
        ).add_to(world_map)

    world_map.save('maps.html')


def create_histogram(dataframe, dep, fuel, target):
    # Ensuring that filters exist by setting default values
    if fuel is None:
        fuel = 'E10'
    if dep is None:
        dep = 94

    # Getting filtered data matching parameters
    data = dataframe.query("prix_nom == '" + fuel + "' and dep_code == '" + str(dep) + "'")[target]
    max_value = data.max()
    min_value = data.min()

    # Preparing the graph
    return px.histogram(data,
                        x=target,
                        height=335,
                        labels={'prix_valeur': 'Prix (€)', 'count': 'Stations (unité)'},
                        range_x=[min_value, max_value],
                        nbins=50,
                        histnorm='density',
                        color_discrete_sequence=['indianred']
                        )
