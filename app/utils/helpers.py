import re
from typing import Union, List
import h3

def parse_speed(speed: Union[str, int, float, List[Union[str, int, float]]]) -> int:
    if isinstance(speed, list):
        speed = speed[0]
    if isinstance(speed, str):
        match = re.search(r'\d+', speed)
        if match:
            return int(match.group())
    elif isinstance(speed, (int, float)):
        return int(speed)
    return 30

def process_road_speeds(resolution: int) -> Dict[str, float]:
    edge_speeds = {}
    for _, _, data in G.edges(data=True):
        speed = parse_speed(data.get("maxspeed", 30))
        geometry = data.get("geometry")
        if geometry:
            coordinates = list(geometry.coords)
            for i in range(len(coordinates) - 1):
                lng1, lat1 = coordinates[i]
                lng2, lat2 = coordinates[i + 1]
                start = h3.geo_to_h3(lat1, lng1, resolution)
                end = h3.geo_to_h3(lat2, lng2, resolution)
                if start != end:
                    try:
                        cells = h3.h3_line(start, end)
                        for j in range(len(cells) - 1):
                            edge = h3.get_h3_unidirectional_edge(cells[j], cells[j + 1])
                            if edge not in edge_speeds or speed > edge_speeds[edge]:
                                edge_speeds[edge] = speed
                    except h3.H3Error:
                        continue
    return edge_speeds