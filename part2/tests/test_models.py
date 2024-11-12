import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

# Test User creation
user = User(first_name="Alice", last_name="Smith", email="alice@example.com")
print(f"User: {user.first_name} {user.last_name}, Email: {user.email}")

# Test Place creation and linking with User
place = Place(title="Cozy Apartment", description="A nice place", price=120.0, latitude=37.7749, longitude=-122.4194, owner=user)
print(f"Place: {place.title}, Price: {place.price}, Owner: {place.owner.first_name}")

# Test adding a Review
review = Review(text="Great place!", rating=5, place=place, user=user)
place.add_review(review)
print(f"Place Reviews: {[r.text for r in place.reviews]}")

# Test adding an Amenity
amenity = Amenity(name="Wi-Fi")
place.add_amenity(amenity)
print(f"Place Amenities: {[a.name for a in place.amenities]}")