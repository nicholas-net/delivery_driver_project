

class Package:
    def __init__(self, id, address, city, state, zip_code, deadline, weight, status="At Hub", timestamp=None):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip_code
        self.deadline = deadline
        self.weight = weight
        self.status = status
        self.timestamp = timestamp

    def __str__(self):
        return f" {self.id}, {self.address}, {self.city}, {self.state}, {self.zip}, {self.deadline}, {self.weight}, {self.status}, {self.timestamp}"

    def __repr__(self):
        return f"{self.address}, {self.city}, {self.state}, {self.zip}, {self.deadline}, {self.weight}, {self.status}, {self.timestamp}"

    def get(self):
        return self.id, self.address, self.city, self.state, self.zip, self.deadline, self.weight, self.status, self.status, self.timestamp


