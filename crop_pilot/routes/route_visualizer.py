import folium
import random

def generate_route_map(points_data, optimized_route, output_file="mapa_rotas.html"):
    depot_point = next(p for p in points_data if p['is_depot'])
    mapa = folium.Map(
        location=[depot_point['latitude'], depot_point['longitude']], 
        zoom_start=15,
        tiles='OpenStreetMap'
    )
    coords_map = {p['name']: (p['latitude'], p['longitude']) for p in points_data}
    colors = ['blue', 'green', 'red', 'purple', 'orange', 'darkred', 'cadetblue']

    for i, trip in enumerate(optimized_route):
        color = colors[i % len(colors)]
        trip_coords = [coords_map[name] for name in trip]
        
        folium.PolyLine(
            trip_coords, 
            color=color, 
            weight=4, 
            opacity=0.8,
            tooltip=f"Viagem {i+1}"
        ).add_to(mapa)

    for p in points_data:
        icon_color = 'black' if p['is_depot'] else 'gray'
        folium.Marker(
            location=[p['latitude'], p['longitude']],
            popup=f"{p['name']} (Carga: {p.get('estimated_load', 0)}kg)",
            icon=folium.Icon(color=icon_color, icon='info-sign')
        ).add_to(mapa)


    mapa.save(output_file)
    print(f"Mapa gerado com sucesso: {output_file}")
