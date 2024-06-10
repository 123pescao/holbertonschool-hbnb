

class City:
    def __init__(self, city_name, country, places):

        self.city_name = city_name
        self.country = country
        self.places = []

    def add_city(self, city):
        self.city_name.append(city)
        self.places.append(city)



class Country(City):
    def __init__(self, country, city_name, places):

        self.country = country
        self.city_name = []
        self.places = []
