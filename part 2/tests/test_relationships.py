import unittest
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class TestModels(unittest.TestCase):

    def test_user_creation(self):
        alice = User(
            first_name="Alice", last_name="Smith", email="alice@example.com"
        )
        self.assertEqual(alice.first_name, "Alice")
        self.assertEqual(alice.last_name, "Smith")
        self.assertEqual(alice.email, "alice@example.com")

    def test_place_creation(self):
        owner = User(
            first_name="Alice", last_name="Smith", email="alice@example.com"
        )
        beach_house = Place(
            title="Beach House",
            description="Seaside house",
            price=100.0,
            latitude=34.0194,
            longitude=-118.4912,
            owner=owner
        )
        self.assertEqual(beach_house.title, "Beach House")
        self.assertEqual(beach_house.description, "Seaside house")
        self.assertEqual(beach_house.price, 100.0)
        self.assertEqual(beach_house.latitude, 34.0194)
        self.assertEqual(beach_house.longitude, -118.4912)
        self.assertEqual(beach_house.owner, owner)

    def test_add_amenity_to_place(self):
        owner = User(
            first_name="Alice", last_name="Smith", email="alice@example.com"
        )
        beach_house = Place(
            title="Beach House",
            description="Seaside house",
            price=100.0,
            latitude=34.0194,
            longitude=-118.4912,
            owner=owner
        )
        wifi = Amenity(name="Wi-Fi")
        beach_house.add_amenity(wifi)
        self.assertIn(wifi, beach_house.amenities)

    def test_add_review_to_place(self):
        owner = User(
            first_name="Alice", last_name="Smith", email="alice@example.com"
        )
        beach_house = Place(
            title="Beach House",
            description="Seaside house",
            price=100.0,
            latitude=34.0194,
            longitude=-118.4912,
            owner=owner
        )
        review = Review(
            text="Great place!",
            rating=5,
            place=beach_house,
            user=owner
        )
        self.assertEqual(review.text, "Great place!")
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.place, beach_house)
        self.assertEqual(review.user, owner)

    def test_amenity_creation(self):
        wifi = Amenity(name="Wi-Fi")
        self.assertEqual(wifi.name, "Wi-Fi")

if __name__ == "__main__":
    unittest.main()
