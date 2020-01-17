from geopy.distance import geodesic
newport_ri = (41.49008, -71.312796)
cleveland_oh = (41.499498, -81.695391)
print(geodesic(newport_ri, cleveland_oh).miles)


from geopy import distance, location

london = location.Point(51.5074, 0.1278)
paris = location.Point(48.8566, -2.3522)

brighton = distance.geodesic().destination(
    point=london,
    bearing=180,
    distance=distance.Distance(kilometers=76))

print("london-paris:", distance.distance(london, paris).kilometers)
print("brighton-paris:", distance.distance(brighton, paris).kilometers)
