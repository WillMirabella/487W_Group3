from models.car import Car
from models.user import User
import db
from datetime import datetime

# Delete all relations
db.clear_relations()

# Create relations
db.create_relations()

# Create user 1 and car 1
u = User(None,"John", "Doe", "1234567890", "jd@gmail.com", "male", "This is my description.", 2028, "Computer Science", None)
c = Car(None,"Toyota", "Camry", "Black", 2024, 4)

# Make user 1 a driver and link the user to car 1
u.make_driver("123 School Ln", "Cash", c.id)

# Create user 2
u2 = User(None,"Bob", "Smith", "1234567890", "bs@gmail.com", "male", "This is my description.", 2028, "Computer Science", None)

# Create user 3 and car 2
u3 = User(None,"Alice", "Jones", "1234567890", "jd@gmail.com", "female", "This is my description.", 2028, "Computer Science", None)
c2 = Car(None,"Toyota", "Prius", "White", 2021, 4)

# Make user 3 a driver and link the user to car 2
u3.make_driver("456 School Ln", "Venmo", c.id)

contact1 = db.insert_contact(u.id, u2.id, "text", datetime.now())
contact2 = db.insert_contact(u3.id, u2.id, "email", datetime.now())

#print(db.get_contact_by_id(contact1))
#print(db.get_contact_by_id(contact2))

"""
Resulting relations:

users:

    id|first_name|last_name|phone|email|gender|description|grad_year|major|schedule|address|preferred_payment|car_id
    --+----------+---------+-----+-----+------+-----------+---------+-----+--------+-------+-----------------+-------
    1 |John      |Doe      |12...|jd...|male  |this is ...|2028     |co...|...     |123 ...|Cash             |1     
    2 |Bob       |Smith    |12...|bs...|male  |this is ...|2028     |co...|...     |       |                 |      
    3 |Alice     |Jones    |12...|aj...|female|this is ...|2028     |co...|...     |456 ...|Venmo            |2     

    Primary Key: id
    Foreign Key: car_id -> cars(id)

cars:

    id|make|model|color|year|capacity
    --+----+-----+-----+----+--------
    1 |t...|ca...|bl...|2024|4            
    2 |t...|pr...|wh...|2021|4          

    Primary Key: id

contacts:

    id|sender|receiver|method|datetime
    --+------+--------+------+--------
    1 |1     |2       |text  |2026-...
    2 |3     |2       |email |2026-...

    Primary Key: id
    Foreign Keys: sender -> users(id), receiver -> users(id)
"""