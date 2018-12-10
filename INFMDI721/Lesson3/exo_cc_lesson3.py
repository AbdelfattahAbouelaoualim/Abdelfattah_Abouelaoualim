from geopy.distance import great_circle
import json


if __name__ == "__main__":
    depart = input("entrez la ville de départ: ")
    arrivee = input("entrez la ville de destination: ")
    with open("cities.json", "r") as file_:
        data = json.load(file_)
    depart_find = False
    arrivee_find = False
    depart_ = []
    arrivee_ = []
    for i in range(len(data)):
        if data[i]["name"].lower() == depart.lower() and len(depart_) < 2:
            depart_.append(data[i]["gps_lat"])
            depart_.append(data[i]["gps_lng"])
            depart_find = True
        if data[i]["name"].lower() == arrivee.lower() and len(arrivee_) < 2:
            arrivee_.append(data[i]["gps_lat"])
            arrivee_.append(data[i]["gps_lng"])
            arrivee_find = True
        if arrivee_find and depart_find:
            break

    depart_ = tuple(depart_)
    arrivee_ = tuple(arrivee_)
    if arrivee_find and depart_find:
        print(f"La distance entre {depart} et {arrivee} est {great_circle(depart_, arrivee_).kilometers} Km")
    elif not arrivee_find:
        print("La ville d'arrivée n'existe pas!")
    elif not depart_find:
        print("La ville de départ n'existe pas!")
    else:
        print("Les villes n'existent pas!")



