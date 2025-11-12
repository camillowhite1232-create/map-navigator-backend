from flask import Flask, jsonify, request
from flask_cors import CORS 
import networkx as nx 
import os 
# import json # Not strictly needed

# --- FLASK APP INITIALIZATION ---
# This line is crucial for Gunicorn to find the 'app' attribute
app = Flask(__name__) 
CORS(app) 

# --- DSA Implementation: Graph Setup ---
# Nodes are cities, weights are hypothetical distances (in km)
G = nx.Graph()
G.add_weighted_edges_from([
    ('Mumbai', 'Delhi', 1400),
    ('Delhi', 'Kolkata', 1500),
    ('Mumbai', 'Chennai', 1200),
    ('Chennai', 'Bangalore', 350),
    ('Bangalore', 'Mumbai', 1000),
    ('Kolkata', 'Hyderabad', 1200),
    ('Hyderabad', 'Bangalore', 570),
    ('Delhi', 'Hyderabad', 1550) 
])

# Coordinates for visualization
NODE_COORDINATES = {
    'Delhi': [28.6139, 77.2090], 
    'Mumbai': [19.0760, 72.8777],
    'Kolkata': [22.5726, 88.3639],
    'Chennai': [13.0827, 80.2707],
    'Bangalore': [12.9716, 77.5946],
    'Hyderabad': [17.3850, 78.4867]
}

@app.route('/api/shortest_path', methods=['POST'])
def find_path():
    """Finds shortest path between two nodes using Dijkstra's Algorithm."""
    data = request.get_json()
    start_node = data.get('start', '').strip()
    end_node = data.get('end', '').strip()

    if not start_node or not end_node:
        return jsonify({"error": "Start and end locations are required."}), 400
    
    if start_node not in G.nodes or end_node not in G.nodes:
        return jsonify({"error": "One or both locations are not recognized on the network. Try: Mumbai, Delhi, Kolkata, Chennai, Bangalore, Hyderabad."}), 404

    try:
        # DSA Calculation (Dijkstra's)
        path = nx.dijkstra_path(G, source=start_node, target=end_node, weight='weight')
        distance = nx.dijkstra_path_length(G, source=start_node, target=end_node, weight='weight')

        path_coordinates = [NODE_COORDINATES[node] for node in path]

        return jsonify({
            "path_name": path, 
            "distance_km": f"{distance:,.0f} km",
            "path_coordinates": path_coordinates,
            "algorithm": "Dijkstra's Shortest Path"
        })
        
    except nx.NetworkXNoPath:
        return jsonify({"error": f"No direct route found between {start_node} and {end_node}."}), 404
    
    except Exception:
        return jsonify({"error": "An internal server error occurred."}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
