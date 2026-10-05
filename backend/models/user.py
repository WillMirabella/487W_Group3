from car import Car

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
        self.schedule = [[None] * 48 for _ in range(5)] # Empty schedule
        self.car_id = None # Foreign Key

        self.user_id = self.to_db() # Primary Key

    def __str__(self):
        # Format schedule
        DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday"]
        result = []
        for day_index, day in enumerate(DAYS):
            result.append(f"\t{day}:")
            for slot_index in range(48):
                if self.schedule[day_index][slot_index] is not None:
                    hour = slot_index // 2
                    minute = (slot_index % 2) * 30
                    result.append(f"\t\t{hour:02d}:{minute:02d} - {"Mandatory" if self.schedule[day_index][slot_index] else "Optional"}")
        schedule_str = "\n" + "\n".join(result)

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
              "\nschedule: " + schedule_str +

              "\ncar_id: " + str(self.car_id))


    # Promotes a user to a driver by filling in extra fields
    def make_driver(self, address, preferred_payment, schedule, make, model, color, year, capacity):
        self.address = address
        self.preferred_payment = preferred_payment
        self.schedule = schedule
        self.car_id = Car(make,model,color,year,capacity, self.user_id).car_id

    
    def set_availability(self, available, weekday, start_time, end_time):
        """
        Sets the availability of the user for a specific day and time range.

        :param available: True for mandatory, False for optional, None for unavailable
        :param weekday: Integer representing the day of the week (0=Monday, 4=Friday)
        :param start_time: Start time in hours (0-24)
        :param end_time: End time in hours (0-24)
        """
        # Time validity checks
        if start_time >= end_time:
            raise ValueError("Start time must be less than end time")
        elif start_time < 0 or end_time > 24:
            raise ValueError("Start time and end time must be between 0 and 24")
        elif start_time == end_time:
            raise ValueError("Start time and end time cannot be the same")
        elif start_time % .5 != 0 or end_time % .5 != 0:
            raise ValueError("Start time or end time too precise")
        # Weekday validity check
        elif weekday < 0 or weekday > 4:
            raise ValueError("Weekday must be between 0 and 4 (0=Monday, 4=Friday)")

        # Convert hours to half-hour slots
        start_slot = int(start_time * 2)
        end_slot = int(end_time * 2)

        # Set the availability for the specified time slots
        for i in range(start_slot, end_slot):
            self.schedule[weekday][i] = available

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

User1.set_availability(True, 0, 1, 3)
User1.set_availability(False, 0, 2, 4)
User1.set_availability(None, 0, 1.5, 2.5)
print(User1)