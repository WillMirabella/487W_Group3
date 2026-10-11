from models.car import Car
import db

class User:
    def __init__(self, id, first_name, last_name, phone, email, gender, description, grad_year, major, schedule):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.gender = gender
        self.description = description
        self.grad_year = grad_year
        self.major = major
        if(schedule==None): self.schedule = [None] * 5 # List of tuples (start_time, end_time) for each weekday (0=Monday, 4=Friday)
        else: self.schedule=schedule
        self.address = None
        self.preferred_payment = None
        self.car_id = None
        if(id == None): self.id = self.to_db() # Primary Key
        else: self.id = id

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

        return ("id: " + str(self.id) +
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


    # Promotes a user to a driver by filling in extra fields and links a user to a specified car
    def make_driver(self, address, preferred_payment,car_id):
        self.address = address
        self.preferred_payment = preferred_payment
        self.car_id = car_id

        db.update_user(self)

    
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

    # Creates a user object from a row of the db
    @classmethod
    def from_db(cls, id):
        row = db.get_user_by_id(id)
        new_user = User(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
        if(car_id!=None): new_user.make_driver(row[10], row[11], row[12], row[13])
        return new_user

    # Adds a newly created user to the db and returns its id
    def to_db(self):
        return db.insert_user(self)