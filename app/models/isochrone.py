from heapq import heappush, heappop
from typing import Dict, Union, List
import h3

def calculate_cell_travel_times(point, h3_resolution, edge_speeds_kmh):
    origin = h3.geo_to_h3(point['lat'], point['lng'], h3_resolution)
    queue = [(0, origin)]
    output = {origin: 0}
    inter_cell_dist = None

    while queue:
        travel_time, cell = heappop(queue)
        neighbors = h3.k_ring(cell, 1)
        for neighbor in neighbors:
            if neighbor != cell:
                edge = h3.get_h3_unidirectional_edge(cell, neighbor)
                if edge in edge_speeds_kmh:
                    if inter_cell_dist is None:
                        coord1 = h3.h3_to_geo(cell)
                        coord2 = h3.h3_to_geo(neighbor)
                        inter_cell_dist = h3.point_dist(coord1, coord2, unit='km')
                    minutes = (inter_cell_dist / edge_speeds_kmh[edge]) * 60
                    new_travel_time = travel_time + minutes
                    if neighbor not in output or new_travel_time < output[neighbor]:
                        output[neighbor] = new_travel_time
                        heappush(queue, (new_travel_time, neighbor))
    return output

def create_isochrone(travel_times: Dict[str, float], threshold: float) -> Dict[str, Union[str, Dict[str, Union[str, List[List[List[float]]]]]]]:
    reachable_cells = {cell: time for cell, time in travel_times.items() if time <= threshold}
    multipolygon = h3.h3_set_to_multi_polygon(reachable_cells.keys(), geo_json=True)
    return {
        "type": "Feature",
        "geometry": {
            "type": "MultiPolygon",
            "coordinates": multipolygon
        }
    }

def h3_to_geojson(cell_travel_times):
    features = []
    for h3_index, value in cell_travel_times.items():
        boundary = h3.h3_to_geo_boundary(h3_index, geo_json=True)
        feature = {
            "type": "Feature",
            "properties": {"value": value, "h3Index": h3_index},
            "geometry": {
                "type": "Polygon",
                "coordinates": [boundary]
            }
        }
        features.append(feature)
    return {
        "type": "FeatureCollection",
        "features": features
    }