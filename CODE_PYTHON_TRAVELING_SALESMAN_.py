# -*- coding: utf-8 -*-
"""
Created on Sun Mar 1 20:42:35 2023



"""

print("\033c")  # Pour vider les élements du termnal
import random
import math
import time

depart = "Montpellier" #Choisir la ville de départ
# Les coordonnées géographiques des villes
villes = {
    "Paris": (48.8567, 2.3508),
    "Marseille": (43.2965, 5.3698),
    "Lyon": (45.7640, 4.8357),
    "Toulouse": (43.6045, 1.4440),
    "Nice": (43.7102, 7.2619),
    "Nantes": (47.2181, -1.5528),
    "Strasbourg": (48.5734, 7.7521),
    "Montpellier": (43.6108, 3.8767),
    "Bordeaux": (44.8378, -0.5792),
    "Lille": (50.6293, 3.0573),
    "Rennes": (48.1147, -1.6794),
    "Grenoble": (45.1885, 5.7245),
    "Rouen": (49.4431, 1.0989),
    "Saint-Etienne": (45.4397, 4.3872),
    "Dijon": (47.3216, 5.0415),
    "Nîmes": (43.8374, 4.3601),
    "Villeurbanne": (45.7731, 4.8906),
    "Angers": (47.4784, -0.5602),
    "Saint-Denis": (48.9358, 2.3596),
    "Aix-en-Provence": (43.5297, 5.4474),
    "Brest": (48.3903, -4.486),
    "Limoges": (45.8336, 1.2611),
    "Clermont-Ferrand": (45.7772, 3.087),
    "Amiens": (49.8942, 2.2957),
    "Nancy": (48.6839, 6.1844),
    "Roubaix": (50.6942, 3.1746),
    "Tourcoing": (50.7236, 3.1524),
    "Orléans": (47.9029, 1.9107),
    "Mulhouse": (47.7500, 7.3335),
    "Caen": (49.1828, -0.3715)
}
 
 #calcul de la distance en km en prenant en compte la rotondité de la Terre  
def distance(lat1, lon1, lat2, lon2):
    # rayon de la terre en km
    R = 6371.0
 
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
 
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
 
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
 
    distance_km = R * c
    return distance_km

#definie et calcule la distance totale parcourue et le temps pour la parcourire
def distance_totale(itineraire):
    global meilleurtemps_traj
    dist_totale = 0
    meilleurtemps_traj = 0                     
    for i in range(len(itineraire)-1):
        ville1 = villes[itineraire[i]]
        ville2 = villes[itineraire[i+1]]
        D = distance(ville1[0], ville1[1], ville2[0], ville2[1])
        dist_totale += D
        #la vitesse est déterminée, 50 km/h si la distance est inférieure à 80 km et 120 km/h sinon
        if D < 80 :
           vitesse = 50
        else:
            vitesse = 120
        temps_traj = D/vitesse                       
        meilleurtemps_traj += temps_traj
 
    return dist_totale
     
 
def monte_carlo(villes, nb_iterations):
    #transformation du dictionnaire en liste
    villes_list = list(villes.keys())
    #retirer la ville de départ
    villes_list.remove(depart)
    #ajout ville depart au debut et à la fin
    meilleur_itineraire = [depart] + villes_list + [depart]
    meilleure_distance = distance_totale(meilleur_itineraire)
 
    for i in range(nb_iterations):
        random.shuffle(villes_list)
        itineraire = [depart] + villes_list + [depart]
        dist = distance_totale(itineraire)
      
        if dist < meilleure_distance:
            meilleur_itineraire = itineraire.copy()
            meilleure_distance = dist
    return meilleur_itineraire, meilleure_distance
 
#nombre d'iteration et calcul du temps d'execution du programme 
nb_iterations_list = [10000]
for nb_iterations in nb_iterations_list:
    start_time = time.time()
    meilleur_itineraire, meilleure_distance = monte_carlo(villes, nb_iterations)
    end_time = time.time()

#introduction de la vitesse moyenne et calcul du temps de trajet avec cette vitesse
    vitesse_moyenne = 110
    temps_trajet = meilleure_distance / vitesse_moyenne



#calculer le nombre de jours nécessaires
heures_travail = 12 #en heures
jours = math.ceil(meilleurtemps_traj/heures_travail) #arrondi au nombre entier supérieur

#calcul des vitesse qui varient (entre 50 et 120 km/h)
vitesse_moyenne1 = meilleure_distance / meilleurtemps_traj
temps_trajet2 = meilleurtemps_traj

# Calcul de l'émission totale de CO2
emission_totale = 0
for i in range(len(meilleur_itineraire)-1):
    ville1 = meilleur_itineraire[i]
    ville2 = meilleur_itineraire[i+1]
    D = distance(villes[ville1][0], villes[ville1][1], villes[ville2][0], villes[ville2][1])
    if D <= 400:
        emission_totale += D * 6 / 1000
    else:
        D_elec = 400
        D_therm = D - 400
        emission_totale += D_elec * 6 / 1000 + D_therm * 120 / 1000
#ajout de la consommation de l'essence du voyageur si il consomme environ 7L/100
conso_essence =  0
conso_essence += (meilleure_distance/100) * 7
#ajout de l'information du coût total du voyage en essence si le litre coute 1.97 euro
prix_essence = 0
prix_essence += math.ceil(conso_essence * 1.97)


print("la ville de départ est :",depart)
print(f"Meilleur itinéraire (distance {meilleure_distance:.2f} km) : ")
print(" -> ".join(meilleur_itineraire))
print(f"Temps de trajet (vitesse moyenne {vitesse_moyenne} km/h) : {temps_trajet:.2f} heures")
print(f"Temps de calcul : {(end_time-start_time):.2f} secondes")
print("le temps de trajet avec des vitesses non constantes est:", round(meilleurtemps_traj), "heures")
print("La vitesse moyenne en comptant les trajet de moins de 80km à 50km/h et les trajets superieur à 120km/h est de :", round(vitesse_moyenne1),"km/h")
print("Emission totale de CO2: ", round(emission_totale, 2), " kg")
print("La durée de la tournée est de", jours, "jour(s)")
print("La consommation d'essence pour ce voyage est de {:.2f} litres.".format(conso_essence))
print("le prix de l'essence pour ce voyage sera d'environ {:.2f} euros".format(prix_essence))