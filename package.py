# Definition for a package object
class Package:
    def __init__(self, id, address, city, state, zip_code, deadline, weight, status="At Hub", timestamp=None, truck_id=None):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip_code
        self.deadline = deadline
        self.weight = weight
        self.status = status
        self.timestamp = timestamp
        self.truck_id = truck_id
    # String representation for a package

    def __str__(self):
            return f" [{self.truck_id}] {self.address}, {self.city}, {self.state} {self.zip} | Deadline: {self.deadline} | Weight: {self.weight} lbs | {self.status}: {self.timestamp}"


