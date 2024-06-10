

class Places:

    def __init__(self, place_id, name, description, address, number_rooms, reviews, bathrooms, price, max_guests):
        self.set_owner = None
        self.place_id = place_id
        self.name = name
        self.description = description
        self.address = address
        self.number_rooms = number_rooms
        self.bathrooms = bathrooms
        self.price = price
        self.max_guests = max_guests
        self.amenities = []
        self.reviews = []
        self.host_name = None
