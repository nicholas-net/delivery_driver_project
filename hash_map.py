from package import Package


class HashMap:
    def __init__(self, capacity=41):
        """Initialize hash map with capacity of 41 (prime number)"""
        self.__capacity = capacity
        self.map = [None] * self.__capacity

    def __str__(self) -> str:
        """Returns packages as strings for debugging"""
        result = ""
        for i in range(len(self.map)):
            result+=f"Index {i}: {self.map[i]}\n"
        return result

    def __repr__(self) -> str:
        return self.__str__()


    def _hash_converter(self, package_id: int) -> int:
            """
            Converts package id into hash between 0 and arrays capacity

            Parameters:
                package id (int) - unique identifier for recipients order
            Return:
                index indicating the packages location on the hash map
            """
            return package_id % self.__capacity

    def insert(self, package_id: int, package_obj: Package) -> None:
        """
        Inserts a package object into the hash map

        Parameters:
            package id (int) - unique identifier used to determine the hash bucket
            package_obj (package) - package instance containing all the delivery data

        """
        hashed_id = self._hash_converter(package_id)
        delivery_data = [package_id, package_obj]

        if self.map[hashed_id] is None:
            self.map[hashed_id] = [delivery_data]

        else:
            self.map[hashed_id].append(delivery_data)

    def package_lookup(self, package_id: int) -> Package:
        """
        Returns the desired package information

        Parameters:
        package_id (int) - unique identifier to the package
        """

        hash_bucket = self._hash_converter(package_id) % self.__capacity
        hash_bucket_list = self.map[hash_bucket]

        for i in range(len(hash_bucket_list)):
            if package_id == hash_bucket_list[i][0]:
                return hash_bucket_list[i][1]

        raise Exception(f"{package_id} not found")









