
#Definition for a package object
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
    # Status of the delivery dictate the format of how the package is printed
        if self.status == "En Route":
            return f" [{self.truck_id}] {self.address}, {self.city}, {self.state} {self.zip} | Deadline: {self.deadline} | Weight: {self.weight} lbs | {self.status}"
        elif self.status == "Delayed":
            return f" {self.address}, {self.city}, {self.state} {self.zip} | Deadline: {self.deadline} | Weight: {self.weight} lbs | {self.status}"
        elif self.status == "At the Hub":
            return f" {self.address}, {self.city}, {self.state} {self.zip} | Deadline: {self.deadline} | Weight: {self.weight} lbs | {self.status}"

        else:
            return f" [{self.truck_id}] {self.address}, {self.city}, {self.state} {self.zip} | Deadline: {self.deadline} | Weight: {self.weight} lbs | {self.status}: {self.timestamp}"


