from package import Package
# Definition for a hash map data structure
class HashMap:
    def __init__(self, capacity=41):
        # Initialize hash map with capacity of 41 (prime number).
        self.__capacity = capacity
        self.map = [None] * self.__capacity


    def _hash_converter(self, package_id: int) -> int:
            """
            Converts package id into hash between 0 and arrays capacity.

            Args:
                package_id (int): unique identifier for recipients order.

            Returns:
                int: index that corresponds to the packages location within the hash map.
            """
            return package_id % self.__capacity


    def insert(self, package_id: int, package_obj: Package) -> None:
        """
        Package ID finds a open bucket within the hash map and inserts the package.

        Args:
            package_id (int): packages unique identifier.
            package_obj (obj): package instance.
        """
        # Hash map index for this package id
        hashed_id = self._hash_converter(package_id)
        # Package ID and object grouped into a pair for storage in a bucket
        delivery_data = [package_id, package_obj]

        if self.map[hashed_id] is None:
            self.map[hashed_id] = [delivery_data]

        else:
            self.map[hashed_id].append(delivery_data)

    def package_lookup(self, package_id: int) -> Package:
        """
        Provides a way to directly access individual packages from the hash map buckets

        Args:
            package_id (int) : unique identifier to the package

        Returns:
            Package: package object
        """

        hash_bucket = self._hash_converter(package_id) % self.__capacity
        hash_bucket_list = self.map[hash_bucket]

        for i in range(len(hash_bucket_list)):
            if package_id == hash_bucket_list[i][0]:
                return hash_bucket_list[i][1]

        raise Exception(f"{package_id} not found")


    def get_all_packages(self):
        all_packages = []
        for bucket in self.map:
            if bucket is not None:
                for entry in bucket:
                    all_packages.append(entry[1])
        return all_packages








