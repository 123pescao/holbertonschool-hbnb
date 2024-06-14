#!/usr/bin/python3
from flask import Flask, request, jsonify, make_response
from persistence.data_manager import DataManager
from models.amenity import Amenity

app = Flask(__name__)
data_manager = DataManager()

@app.route('/amenities', methods=['POST'])
def create_amenity():
    data = request.json
    if "name" not in data or not data["name"].strip():
        return make_response(jsonify({"error": "Invalid missing amenity name"}), 400)

    try:
        amenity = Amenity(name=data["name"])
        data_manager.save(amenity)
        return make_response(jsonify(amenity.__dict__), 201)
    except ValueError as e:
        return make_response(jsonify({"error": str(e)}), 409)

@app.route('/amenities', methods=['GET'])
def get_amenities():
    amenities = list(data_manager.storage["Amenity"].values())
    return jsonify([amenity.__dict__ for amenity in amenities])

@app.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    amenity = data_manager.get(amenity_id, "Amenity")
    if amenity is None:
        return make_response(jsonify({"error": "Amenity not found"}), 404)
    return jsonify(amenity.__dict__)

@app.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    data = request.json
    amenity = data_manager.get(amenity_id, "Amenity")
    if amenity is None:
        return make_response(jsonify({"error": "Amenity not found"}), 404)

    if "name" in data and not data["name"].strip():
        return make_response(jsonify({"error": "Invalid amenity name"}), 400)

    try:
        amenity.update(name=data.get("name"))
        data_manager.update(amenity)
        return jsonify(amenity.__dict__)
    except ValueError as e:
        return make_response(jsonify({"error": str(e)}), 409)

@app.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    amenity = data_manager.get(amenity_id, "Amenity")
    if amenity is None:
        return make_response(jsonify({"error": "Amenity not found"}), 404)

    data_manager.delete(amenity_id, "Amenity")
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
