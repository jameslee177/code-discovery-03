from flask import Flask, jsonify
import json

app = Flask(__name__)

# Load sample data from an external JSON file
with open('mock_data.json', 'r') as f:
    mock_data = json.load(f)

# Load API route dynamically from an external file
with open('external_routes.json', 'r') as f:
    external_route = json.load(f)

# Explicitly defined APIs
@app.route('/api/users', methods=['GET'])
def get_users():
    """
    Fetch all users from the external JSON file.
    """
    users = mock_data.get("users", {})
    return jsonify(users)


@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Fetch a specific user by ID from the external JSON file.
    """
    user = mock_data.get("users", {}).get(str(user_id))
    if user:
        return jsonify(user)
    else:
        return jsonify({"error": "User not found"}), 404


# Dynamically register the external route
@app.route(external_route["path"], methods=[external_route["method"].upper()])
def dynamic_route():
    """
    Fetch data for a dynamically defined route.
    """
    resource_key = external_route["path"].split("/")[-1]
    resource_data = mock_data.get(resource_key, {})
    return jsonify(resource_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
