from car import Car
from schedule import Schedule

class User:
    def __init__(self, first_name, last_name, phone, email, gender, description, grad_year, major):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.gender = gender
        self.description = description
        self.grad_year = grad_year
        self.major = major

        self.address = None
        self.preferred_payment = None
        self.schedule = Schedule()
        self.car_id = None # Foreign Key

        self.user_id = self.to_db() # Primary Key

    def __str__(self):
        return ("user_id: " + str(self.user_id) +
              "\nfirst_name: " + self.first_name +
              "\nlast_name: " + self.last_name +
              "\nphone: " + str(self.phone) +
              "\nemail: " + self.email +
              "\ngender: " + self.gender +
              "\ndescription: " + self.description +
              "\ngrad_year: " + str(self.grad_year) +
              "\nmajor: " + self.major +

              "\naddress: " + str(self.address) +
              "\npreferred_payment: " + str(self.preferred_payment) +
              "\nschedule: \n" + str(self.schedule) +

              "\ncar_id: " + str(self.car_id))


    # Promotes a user to a driver by filling in extra fields
    def make_driver(self, address, preferred_payment, schedule, make, model, color, year, capacity):
        self.address = address
        self.preferred_payment = preferred_payment
        self.schedule = schedule
        self.car_id = Car(make,model,color,year,capacity, self.user_id).car_id

    # Needs implementation
    # Creates a user object from a row of the db
    @classmethod
    def from_db(cls):
        return

    # Needs implementation
    # Adds a newly created user to the db (return the user_id that is chosen to use in constructor)
    def to_db(self):
        return 1
    
User1 = User("John", "Doe", "1234567890", "john.doe@example.com", "Male", "I am a student", 2025, "Computer Science")
print(User1)