from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory user data
users = [
    {"id": 1, "name": "John int", "email": "john@int.com"},
    {"id": 2, "name": "Jane float", "email": "jane@float.com"}
]

# Helper: Find user by ID
def find_user(user_id):
    return next((user for user in users if user["id"] == user_id), None)

# GET all users
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

# GET single user
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = find_user(user_id)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

# POST new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    if not data.get("name") or not data.get("email"):
        return jsonify({"error": "Missing name or email"}), 400

    new_id = max(user["id"] for user in users) + 1 if users else 1
    new_user = {"id": new_id, "name": data["name"], "email": data["email"]}
    users.append(new_user)
    return jsonify(new_user), 201

# PUT update user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = find_user(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.json
    user["name"] = data.get("name", user["name"])
    user["email"] = data.get("email", user["email"])
    return jsonify(user)

# DELETE user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = find_user(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    users.remove(user)
    return jsonify({"message": "User deleted successfully"})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
