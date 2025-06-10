
class HashMap:
    MAP_CAPACITY = 41
    def __init__(self):
        self.capacity =  MAP_CAPACITY
        self.map = [None] * self.capacity


    # Provides a valid index to store in the hash map
    def hash_convertor(self, package_id: int) -> int:
            """
            Parameters:
                self - referring to the hash map instance
                Package ID - unique identifier for recipients order
            Return:
                Index indicating the packages location on the hash map
            """
            return package_id % self.capacity





