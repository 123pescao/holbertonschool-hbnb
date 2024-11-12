#!/usr/bin/python3
"""HBnB Facade"""
import re
from app.persistence.repository import InMemoryRepository, SQLAlchemyRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app import bcrypt  # Import bcrypt to hash passwords

class HBnBFacade:
    def __init__(self):
        self.user_repo = SQLAlchemyRepository(User)
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

    def _is_valid_email(self, email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

    # User methods
    def create_user(self, user_data):
        required_user_fields = ['first_name', 'last_name', 'email', 'password']
        for field in required_user_fields:
            if not user_data.get(field, "").strip():
                raise ValueError(f"{field} cannot be empty.")

        if not self._is_valid_email(user_data['email']):
            raise ValueError("Invalid email format.")

        # Hash the password before storing the user
        hashed_password = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')
        user_data['password'] = hashed_password
        # Set the `is_admin` value explicitly as 0 or 1
        user_data['is_admin'] = bool(user_data.get('is_admin', False))

        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        user = self.user_repo.get(user_id)
        if user:
            # Remove password before returning user data
            del user.password
        return user

    def get_all_users(self):
        users = self.user_repo.get_all()
        # Remove password from all user data before returning
        for user in users:
            del user.password
        return users

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if user:
            if 'password' in user_data:
                # Hash the new password before updating
                user_data['password'] = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')

            for key, value in user_data.items():
                setattr(user, key, value)

            # Remove password before returning updated user
            del user.password
            return user
        return None

    # Amenity methods
    def create_amenity(self, amenity_data):
        required_amenity_fields = ['name']
        for field in required_amenity_fields:
            if field not in amenity_data:
                raise ValueError(f"Missing required field: '{field}'")
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if amenity:
            for key, value in amenity_data.items():
                setattr(amenity, key, value)
            return amenity
        return None

    # Place methods
    def create_place(self, place_data):
        required_place_fields = ['title', 'owner_id', 'price', 'latitude', 'longitude']
        for field in required_place_fields:
            if field not in place_data:
                raise ValueError(f"'{field}' cannot be empty")

        # Validate price is positive
        if place_data['price'] <= 0:
            raise ValueError("Price must be a positive number.")

        # Validate latitude and longitude ranges
        if not (-90 <= place_data['latitude'] <= 90):
            raise ValueError("Latitude must be between -90 and 90.")
        if not (-180 <= place_data['longitude'] <= 180):
            raise ValueError("Longitude must be between -180 and 180.")

        # Validate owner existence
        owner_id = place_data['owner_id']
        if not self.user_repo.get(owner_id):
            raise ValueError("Invalid owner_id: Owner does not exist.")

        # Set default empty amenities list if not provided
        place_data.setdefault('amenities', [])

        # Create and add place
        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        if place:
            # Retrieve associated owner and amenities
            place.owner = self.user_repo.get(place.owner_id)
            place.amenities = [self.amenity_repo.get(a_id) for a_id in place.amenities if self.amenity_repo.get(a_id)]
        return place

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            return None

        # Update attributes and validate amenities
        for key, value in place_data.items():
            if key == "amenities":
                # Update amenities with valid IDs only
                place.amenities = [a_id for a_id in value if self.amenity_repo.get(a_id)]
            else:
                setattr(place, key, value)
        return place

    # Review Methods
    def create_review(self, review_data):
        required_fields = ['text', 'rating', 'user_id', 'place_id']
        for field in required_fields:
            if not review_data.get(field):
                raise ValueError(f"'{field}' cannot be empty.")

        if not (1 <= review_data['rating'] <= 5):
            raise ValueError("Rating must be between 1 and 5.")

        user = self.user_repo.get(review_data['user_id'])
        place = self.place_repo.get(review_data['place_id'])
        if not user:
            raise ValueError("Invalid user_id: User does not exist.")
        if not place:
            raise ValueError("Invalid place_id: Place does not exist.")

        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        return [review for review in self.review_repo.get_all() if review.place_id == place_id]

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        for key, value in review_data.items():
            setattr(review, key, value)
        return review

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if review:
            self.review_repo.delete(review_id)
            return True
        return False
