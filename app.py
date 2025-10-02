from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

# In-memory storage for dynamic routes
routes = {}

@app.route('/healthz')
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "ok"})

@app.route('/A')
def hello_world():
    """Hello world endpoint"""
    return jsonify({"message": "hello world"})

@app.route('/admin/routes', methods=['POST'])
def create_route():
    """Create a new route with static JSON response"""
    # Check API key
    api_key = request.headers.get('X-API-Key')
    if api_key != 'admin-secret-key-123':
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.get_json()
    if not data or 'path' not in data or 'message' not in data:
        return jsonify({"error": "Missing path or message"}), 400
    
    path = data['path']
    message = data['message']
    
    # Store the route
    routes[path] = message
    
    return jsonify({
        "message": f"Route {path} created successfully",
        "path": path
    })

@app.route('/admin/routes', methods=['GET'])
def list_routes():
    """List all created routes"""
    # Check API key
    api_key = request.headers.get('X-API-Key')
    if api_key != 'admin-secret-key-123':
        return jsonify({"error": "Unauthorized"}), 401
    
    route_list = [{"path": path, "message": message} for path, message in routes.items()]
    return jsonify({
        "routes": route_list,
        "count": len(route_list)
    })

@app.route('/admin/routes/<path:route_path>', methods=['DELETE'])
def delete_route(route_path):
    """Delete a route"""
    # Check API key
    api_key = request.headers.get('X-API-Key')
    if api_key != 'admin-secret-key-123':
        return jsonify({"error": "Unauthorized"}), 401
    
    if route_path not in routes:
        return jsonify({"error": "Route not found"}), 404
    
    del routes[route_path]
    return jsonify({"message": f"Route /{route_path} deleted successfully"})

# Dynamic route handler for created routes
@app.route('/<path:route_path>')
def dynamic_route(route_path):
    """Handle dynamically created routes"""
    if route_path in routes:
        return jsonify({"message": routes[route_path]})
    else:
        return jsonify({"error": "Route not found"}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
