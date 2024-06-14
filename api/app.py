# api/app.py
print("Loading app from api/app.py")

from flask import Flask, jsonify, request
from model.places import Place
from model.reviews import Review
from model.amenities import Amenities
from model.city_country import City, Country
from persistence.data_manager import DataManager
from model.user import User

app = Flask(__name__)
data_manager = DataManager()

# Example route
@app.route('/')
def index():
    return jsonify({"message": "Welcome to the HBnB API!"})

# User endpoints
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"error": "Missing user data"}), 400

    try:
        new_user = User(email=data['email'], password=data['password'],
                        first_name=data.get('first_name', ''),
                        last_name=data.get('last_name', ''))
        data_manager.save(new_user)
    except ValueError as e:
        return jsonify({"error": str(e)}), 409

    return jsonify(new_user.to_dict()), 201

@app.route('/users', methods=['GET'])
def get_users():
    users = data_manager.storage.get('User', {}).values()
    return jsonify([user.to_dict() for user in users]), 200

@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = data_manager.get(user_id, 'User')
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict()), 200

@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = data_manager.get(user_id, 'User')
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.update_name(first_name=data.get('first_name', user.first_name),
                     last_name=data.get('last_name', user.last_name))
    data_manager.save(user)
    return jsonify(user.to_dict()), 200

@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = data_manager.get(user_id, 'User')
    if not user:
        return jsonify({"error": "User not found"}), 404

    data_manager.delete(user_id, 'User')
    return '', 204

# Place endpoints
@app.route('/places', methods=['POST'])
def create_place():
    data = request.get_json()
    user = data_manager.get(data.get('host_id'), 'User')
    if not user:
        return jsonify({"error": "Host not found"}), 404

    place = Place(place_id=data.get('place_id'), name=data.get('name'),
                  description=data.get('description'), address=data.get('address'),
                  city=data.get('city'), host=user)
    data_manager.save(place)
    return jsonify(place.to_dict()), 201

@app.route('/places', methods=['GET'])
def get_places():
    places = data_manager.storage.get('Place', {}).values()
    return jsonify([place.to_dict() for place in places]), 200

@app.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    place = data_manager.get(place_id, 'Place')
    if not place:
        return jsonify({"error": "Place not found"}), 404
    return jsonify(place.to_dict()), 200

@app.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    data = request.get_json()
    place = data_manager.get(place_id, 'Place')
    if not place:
        return jsonify({"error": "Place not found"}), 404

    place.name = data.get('name', place.name)
    place.description = data.get('description', place.description)
    place.address = data.get('address', place.address)
    data_manager.save(place)
    return jsonify(place.to_dict()), 200

@app.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    place = data_manager.get(place_id, 'Place')
    if not place:
        return jsonify({"error": "Place not found"}), 404

    data_manager.delete(place_id, 'Place')
    return '', 204

# Review endpoints
@app.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    data = request.get_json()
    user = data_manager.get(data.get('user_id'), 'User')
    place = data_manager.get(place_id, 'Place')
    if not user:
        return jsonify({"error": "User not found"}), 404
    if not place:
        return jsonify({"error": "Place not found"}), 404

    review = Review(review_id=data.get('review_id'), user=user, place=place,
                    rating=data.get('rating'), comment=data.get('comment'))
    data_manager.save(review)
    return jsonify(review.to_dict()), 201

@app.route('/places/<place_id>/reviews', methods=['GET'])
def get_reviews_for_place(place_id):
    place = data_manager.get(place_id, 'Place')
    if not place:
        return jsonify({"error": "Place not found"}), 404

    reviews = [review for review in data_manager.storage.get('Review', {}).values() if review.place.id == place_id]
    return jsonify([review.to_dict() for review in reviews]), 200

@app.route('/users/<user_id>/reviews', methods=['GET'])
def get_reviews_for_user(user_id):
    user = data_manager.get(user_id, 'User')
    if not user:
        return jsonify({"error": "User not found"}), 404

    reviews = [review for review in data_manager.storage.get('Review', {}).values() if review.user.id == user_id]
    return jsonify([review.to_dict() for review in reviews]), 200

@app.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    review = data_manager.get(review_id, 'Review')
    if not review:
        return jsonify({"error": "Review not found"}), 404
    return jsonify(review.to_dict()), 200

@app.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    data = request.get_json()
    review = data_manager.get(review_id, 'Review')
    if not review:
        return jsonify({"error": "Review not found"}), 404

    review.rating = data.get('rating', review.rating)
    review.comment = data.get('comment', review.comment)
    data_manager.save(review)
    return jsonify(review.to_dict()), 200

@app.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    review = data_manager.get(review_id, 'Review')
    if not review:
        return jsonify({"error": "Review not found"}), 404

    data_manager.delete(review_id, 'Review')
    return '', 204

# Amenity endpoints
@app.route('/amenities', methods=['POST'])
def create_amenity():
    data = request.get_json()
    amenity = Amenities(name=data.get('name'))
    data_manager.save(amenity)
    return jsonify(amenity.to_dict()), 201

@app.route('/amenities', methods=['GET'])
def get_amenities():
    amenities = data_manager.storage.get('Amenities', {}).values()
    return jsonify([amenity.to_dict() for amenity in amenities]), 200

@app.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    amenity = data_manager.get(amenity_id, 'Amenities')
    if not amenity:
        return jsonify({"error": "Amenity not found"}), 404
    return jsonify(amenity.to_dict()), 200

@app.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    data = request.get_json()
    amenity = data_manager.get(amenity_id, 'Amenities')
    if not amenity:
        return jsonify({"error": "Amenity not found"}), 404

    amenity.name = data.get('name', amenity.name)
    data_manager.save(amenity)
    return jsonify(amenity.to_dict()), 200

@app.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    amenity = data_manager.get(amenity_id, 'Amenities')
    if not amenity:
        return jsonify({"error": "Amenity not found"}), 404

    data_manager.delete(amenity_id, 'Amenities')
    return '', 204

# City and Country endpoints
@app.route('/countries', methods=['GET'])
def get_countries():
    countries = data_manager.storage.get('Country', {}).values()
    return jsonify([country.to_dict() for country in countries]), 200

@app.route('/countries/<country_code>', methods=['GET'])
def get_country(country_code):
    country = next((country for country in data_manager.storage.get('Country', {}).values() if country.code == country_code), None)
    if not country:
        return jsonify({"error": "Country not found"}), 404
    return jsonify(country.to_dict()), 200

@app.route('/countries/<country_code>/cities', methods=['GET'])
def get_cities_for_country(country_code):
    country = next((country for country in data_manager.storage.get('Country', {}).values() if country.code == country_code), None)
    if not country:
        return jsonify({"error": "Country not found"}), 404

    cities = [city for city in data_manager.storage.get('City', {}).values() if city.country_code == country_code]
    return jsonify([city.to_dict() for city in cities]), 200

@app.route('/cities', methods=['POST'])
def create_city():
    data = request.get_json()
    country = next((country for country in data_manager.storage.get('Country', {}).values() if country.code == data.get('country_code')), None)
    if not country:
        return jsonify({"error": "Country not found"}), 404

    city = City(name=data.get('name'), country_code=data.get('country_code'))
    data_manager.save(city)
    return jsonify(city.to_dict()), 201

@app.route('/cities', methods=['GET'])
def get_cities():
    cities = data_manager.storage.get('City', {}).values()
    return jsonify([city.to_dict() for city in cities]), 200

@app.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    city = data_manager.get(city_id, 'City')
    if not city:
        return jsonify({"error": "City not found"}), 404
    return jsonify(city.to_dict()), 200

@app.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    data = request.get_json()
    city = data_manager.get(city_id, 'City')
    if not city:
        return jsonify({"error": "City not found"}), 404

    city.name = data.get('name', city.name)
    data_manager.save(city)
    return jsonify(city.to_dict()), 200

@app.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    city = data_manager.get(city_id, 'City')
    if not city:
        return jsonify({"error": "City not found"}), 404

    data_manager.delete(city_id, 'City')
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)