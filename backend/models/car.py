class Car:
    def __init__(self, make, model, color, year, capacity, user_id):
        self.make = make
        self.model = model
        self.color = color
        self.year = year
        self.capacity = capacity
        self.user_id = user_id # Foreign Key

        self.car_id = self.to_db() # Primary Key
    
    def __str__(self):
        return ("car_id: " + str(self.car_id) +
              "\nmake: " + self.make +
              "\nmodel: " + self.model +
              "\ncolor: " + self.color +
              "\nyear: " + str(self.year) +
              "\ncapacity: " + str(self.capacity) +
              "\nuser_id: " + str(self.user_id))

    # Needs implementation
    # Creates a car object from a row of the db
    @classmethod
    def from_db(cls, row):
        return

    # Needs implementation
    # Adds a newly created car to the db (return the car_id that is chosen to use in constructor)
    def to_db(self):
        return 1