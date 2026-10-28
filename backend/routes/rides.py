
#These are fake demonstration rides, not actual available drivers!!
from flask import Blueprint, jsonify

rides_bp = Blueprint("rides", __name__, url_prefix="/api/rides")

# Temporary sample data until we connect PostgreSQL.
sample_rides = [
    {
        "id": 1,
        "driver": "Alex Johnson",
        "destination": "King of Prussia Mall",
        "departure_time": "3:30 PM",
        "seats_available": 3,
        "price": 5.00,
    },
    {
        "id": 2,
        "driver": "Jordan Smith",
        "destination": "Philadelphia",
        "departure_time": "4:15 PM",
        "seats_available": 2,
        "price": 8.00,
    },
    {
        "id": 3,
        "driver": "Taylor Brown",
        "destination": "Willow Grove",
        "departure_time": "5:00 PM",
        "seats_available": 1,
        "price": 4.00,
    },
]


@rides_bp.get("/")
def get_rides():
    return jsonify({
        "rides": sample_rides,
        "count": len(sample_rides),
    })
