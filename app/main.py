from app import app
from flask import Flask, request, jsonify
from flask_cors import CORS
import osmnx as ox
import logging
from app.utils import process_road_speeds
from app.models import calculate_cell_travel_times, create_isochrone, h3_to_geojson


app.logger.setLevel(logging.DEBUG)

# Laden Sie das Graph einmal beim Start der Anwendung
G = ox.load_graphml("/app/data/hamburg_road_network.graphml")

@app.route('/')
def hello():
    return "Hello, World!"

@app.route('/calculate_isochrone', methods=['POST'])
def calculate_isochrone():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 415

    try:
        data = request.get_json()
        lat = float(data['lat'])
        lon = float(data['lon'])
        res = int(data['res'])
        threshold = float(data['threshold'])

        edge_speeds = process_road_speeds(G, res)
        travel_times = calculate_cell_travel_times({'lat': lat, 'lng': lon}, res, edge_speeds)

        isochrone = create_isochrone(travel_times, threshold)
        hexagons = h3_to_geojson(travel_times)

        return jsonify({
            'isochrone': isochrone,
            'hexagons': hexagons
        })

    except KeyError as e:
        return jsonify({"error": f"Missing required parameter: {str(e)}"}), 400
    except ValueError as e:
        return jsonify({"error": f"Invalid parameter value: {str(e)}"}), 400
    except Exception as e:
        app.logger.error(f"An error occurred: {str(e)}")
        return jsonify({"error": "An internal server error occurred"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(debug=True)