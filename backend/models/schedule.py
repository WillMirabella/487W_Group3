class Schedule:
    """
    A class to represent a schedule with half-hour precision and mandatory and optional time slots.
    """
    def __init__(self): 
        self.availability = [[None] * 48 for _ in range(5)] # 5 days, 48 half-hour slots per day

    def add_availability(self, is_mandatory, weekday, start_time, end_time):
        # Time validity checks
        if start_time >= end_time:
            raise ValueError("Start time must be less than end time")
        elif start_time < 0 or end_time > 24:
            raise ValueError("Start time and end time must be between 0 and 24")
        elif start_time == end_time:
            raise ValueError("Start time and end time cannot be the same")
        # Weekday validity check
        elif weekday < 0 or weekday > 4:
            raise ValueError("Weekday must be between 0 and 4 (0=Monday, 4=Friday)")

        # Convert hours to half-hour slots
        start_slot = int(start_time * 2)
        end_slot = int(end_time * 2)

        # Set the availability for the specified time slots
        for i in range(start_slot, end_slot):
            self.availability[weekday][i] = is_mandatory

    def __str__(self):
        # TODO: Decide whether Sunday and Saturday should be included
        DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        result = []
        for day_index, day in enumerate(DAYS):
            result.append(f"{day}:")
            for slot_index in range(48):
                if self.availability[day_index][slot_index] is not None:
                    hour = slot_index // 2
                    minute = (slot_index % 2) * 30
                    result.append(f"  {hour:02d}:{minute:02d} - {"Mandatory" if self.availability[day_index][slot_index] else "Optional"}")
        return "\n".join(result)

sched = Schedule()
sched.add_availability(True, 0, 6, 8)
sched.add_availability(False, 0, 7, 9)
print(sched)