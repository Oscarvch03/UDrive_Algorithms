import osmnx as ox
import networkx as nx
import geopy as gp
import folium as fl

ox.config(log_console=True, use_cache=True)
locator = gp.geocoders.Nominatim(user_agent='myapp')
place = 'Bogotá DC, Colombia'
mode = 'drive'
graph = ox.graph_from_place(place, network_type=mode)

def geocode(address):
    location = locator.geocode(address)
    if(location == None):
        return None
    return (location.latitude, location.longitude)

def generate_html_map(p1, d1, p2, d2, route, optimizer, num_request):
    c_edge = 'blue' if optimizer == 'time' else 'red'
    shortest_route_map = ox.plot_route_folium(graph, route, tiles='openstreetmap', color=c_edge)
    fl.Marker(location=p1, popup=d1, tooltip='Clic', icon=fl.Icon(icon='info-sign', color='lightgreen')).add_to(shortest_route_map)
    fl.Marker(location=p2, popup=d2, tooltip='Clic', icon=fl.Icon(icon='info-sign', color='pink')).add_to(shortest_route_map)
    shortest_route_map.save('map{0}{1}'.format(num_request, optimizer[0]))

def routes(p1, d1, p2, d2, optimizer, num_request):
    orig_node = ox.get_nearest_node(graph, p1)
    dest_node = ox.get_nearest_node(graph, p2)
    shortest_route = nx.shortest_path(graph, orig_node, dest_node, weight=optimizer)
    shortest_len = nx.shortest_path_length(graph, orig_node, dest_node, weight=optimizer)
    w = round(shortest_len / 60, 2) if optimizer == 'time' else round(shortest_len / 1000, 2)
    generate_html_map(p1, d1, p2, d2, shortest_route, optimizer, num_request)
    return shortest_route, w


claustro = 'Bogotá DC, La Candelaria, Universidad del Rosario'
mutis = 'Bogotá DC, Barrios Unidos, Universidad del Rosario'
norte = 'Bogotá DC, Usaquén, Universidad del Rosario'
p1 = geocode(claustro)
p2 = geocode(mutis)
p3 = geocode(norte)
print()
print(p1)
print(p2)
print(p3)
print()

cl2mu_t, w1t = routes(p1, claustro, p2, mutis, 'time', 1)
cl2mu_l, w1l = routes(p1, claustro, p2, mutis, 'length', 1)
print()
print(len(cl2mu_t), w1t)
print(len(cl2mu_l), w1l)
print()

cl2no_t, w2t = routes(p1, claustro, p3, norte, 'time', 2)
cl2no_l, w2l = routes(p1, claustro, p3, norte, 'length', 2)
print()
print(len(cl2no_t), w2t)
print(len(cl2no_l), w2l)
print()