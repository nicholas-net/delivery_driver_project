# All code written by Nicholas Colon

import csv
import datetime as dt
from hash_map import HashMap
from package import Package

# Variables act as physical trucks and are manually loaded with package IDs.
TRUCK_1 = [4, 5, 6, 7, 8, 9, 10, 11, 12]
TRUCK_2 = [1, 3, 18, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 36, 38]
TRUCK_3 = [2, 13, 14, 15, 16, 17, 19, 20, 31, 32, 33, 34, 35, 37, 39, 40]

def load_delivery_data(file_name) -> None:
    """
    Each row of the package file contains data on a specific delivery. Each cell of a row.
    is added as an attribute of a package object. The package is then inserted into the hash map.

    Args:
        file_name (str) : package data file.
    """
    with open(file_name) as package_file:
        delivery_data = csv.reader(package_file, delimiter=",")
        for package in delivery_data:
            package_id = int(package[0])
            delivery_address = package[1]
            delivery_city = package[2]
            delivery_state = package[3]
            delivery_zip = package[4]
            delivery_deadline = package[5]
            delivery_weight = package[6]
            package = Package(package_id, delivery_address, delivery_city, delivery_state, delivery_zip, delivery_deadline, delivery_weight)
            hash_map_1.insert(package_id, package)

def load_distance_data(file_name) -> list and dict:
    """
    Float points containing the distances between each address are passed in with a csv file.
    The index for each address is saved in a dictionary with the address name as the value. The first index starts at the first row.
    Each row (with the address now removed) is then inserted as its own element into a separate list.

    Args:
        file_name (str) : distance data file.

    Returns:
        list: floats points indicating the distance between each address in miles.
        dict: address index is the key and address name is the value.
    """
    address_indices = {}
    distances_between_address = []
    with open(file_name) as distance_file:
        distance_table = csv.reader(distance_file, delimiter=",")
        for index, distance in enumerate(distance_table):
            address_indices[distance[0]] = index
            distance.pop(0)
            distances_between_address.append(distance)
        return address_indices, distances_between_address

# Mileage of each truck at the end of its route has to be saved.
truck_miles = {"TRUCK_1": 0, "TRUCK_2": 0, "TRUCK_3": 0}

def delivery(truck: list, time: object, address_dict: dict, distance_floats: list, truck_miles: dict, truck_identifier: str) -> None:
    """
    Truck drives until all packages are delivered to an address. Uses a nearest-neighbor algorithm to decide its route.
    From the trucks current location, it will travel to the next address that takes the least mileage.

    Args:
        truck (list) : the truck the package is one.
        time (object) : the time the package is delivered.
        address_dict (dict) : the index from the distance table that the address is saved in.
        distance_floats (list) : miles between each address.
        truck_miles (dict) : truck mileage tracker.
        truck_identifier (str) : the trucks unique id number.
    """
    THE_HUB = 0
    total_mileage = 0
    current_truck_location = THE_HUB
    TRUCK_SPEED = 18

    # Trucks will keep driving until all packages have a delivered status.
    while any(hash_map_1.package_lookup(package_id).status != "Delivered" for package_id in truck):
        closest_distance = float("inf")
        closest_package_id = None
        closest_address_index = None

        # Gets the package objects delivery data and its index from the distance table.
        for package_id in truck:
            package_obj = hash_map_1.package_lookup(package_id)
            address_index = address_dict[package_obj.address]
            # The data from the table is mirrored so this ensures we don't try to grab a float from an empty cell.
            if package_obj.status != "Delivered":
                if address_index >= current_truck_location:
                    address_distance = float(distance_floats[address_index][current_truck_location])
                else:
                    address_distance = float(distance_floats[current_truck_location][address_index])
                # Saves the closest address, package id and addresses index from the trucks current location.
                if address_distance < closest_distance:
                    closest_distance = address_distance
                    closest_package_id = package_id
                    closest_address_index = address_index
        # Truck moves to the next closest location and "delivers" the package.
        if closest_address_index is not None:
            current_truck_location = closest_address_index
            closest_package = hash_map_1.package_lookup(closest_package_id)
            closest_package.status = "Delivered"
            closest_package.truck_id = truck_identifier
            total_mileage += closest_distance
            time_passed = closest_distance / TRUCK_SPEED
            hours = dt.timedelta(hours=time_passed)
            time += hours
            time_stamp = time.strftime("%I:%M %p")
            closest_package.timestamp = time_stamp

    miles = round(total_mileage, 2)
    truck_miles[truck_identifier] = miles

def _get_status(package: object, input_time: object, truck_start_time: object, delayed_time: object, address_update: object) -> str:
    """
    Helper function that handles the display of each packages status depending on what time the user inputs.
    The delayed packages are a special case because they don't arrive to the hub until a later time.

    Args:
        package (object) : package to be displayed
        input_time (object) : time user enters when prompted by the interface
        truck_start_time (object) : time all trucks leave the hub
        delayed_time (object) : time the delayed packages arrive at the hub
        address_update (object) : time the wrong address is fixed

    Returns:
        str: status of the delayed packages.
    """
    delayed_packages = [6, 25, 28, 32]
    if package.id in delayed_packages and input_time < delayed_time:
        return "Delayed"
    elif input_time < truck_start_time:
        return "At the hub"
    elif package.timestamp:
        delivered_time = dt.datetime.strptime(package.timestamp, "%I:%M %p")
        if input_time < delivered_time:
            return "En Route"
        else:
            return f"Delivered at {package.timestamp}"
    return "En Route"

def package_interface() -> object or float:
    """
    Basic command-line interface to separate the truck information from the delivery info. Converts times into datetime objects
    so they can properly be compared.

    Returns:
        object: the package and its delivery status.
        int: total mileage of the trucks.
    """
    print("Salt Lake City Delivery Service")
    print("---------------------------------")
    print("A: View Delivery Status")
    print("B: Truck mileage")
    print("Q: Quit")
    user_input = input()

    while user_input.upper() != "Q":

        if user_input.upper() == "A":
            print("---------------------------------")
            print("Enter time of day:")
            print("(Format: HH:MM XM)")
            time_request = input()
            print("---------------------------------")
            input_time = dt.datetime.strptime(time_request, "%I:%M %p")
            TRUCK_START_TIME = "8:00 AM"
            truck_start_time = dt.datetime.strptime(TRUCK_START_TIME, "%I:%M %p")

            delayed_time_str = "9:05 AM"
            delayed_time = dt.datetime.strptime(delayed_time_str, "%I:%M %p")

            # One of the addresses was filled out incorrectly by the customer.
            # Depending on the time the user inputs, the destination will be incorrect until 10:20 AM.
            wrong_address_filed = [9]
            address_update_time = "10:20 AM"
            address_update = dt.datetime.strptime(address_update_time, "%I:%M %p")

            for package in hash_map_1.get_all_packages():
                status = _get_status(package, input_time, truck_start_time, delayed_time, address_update)

                if package.id in TRUCK_1:
                    truck_id = "TRUCK 1"
                elif package.id in TRUCK_2:
                    truck_id = "TRUCK 2"
                else:
                    truck_id = "TRUCK 3"

                if package.id in wrong_address_filed and input_time < address_update:
                    display_address = "300 State St"
                else:
                    display_address = package.address

                print(f"[{truck_id}] | ID: {package.id} | {display_address}, {package.city}, {package.state} {package.zip} | Deadline: {package.deadline} | Weight: {package.weight} lbs | Status: {status}")

        elif user_input == "B":
            print("---------------------------------")
            print("Miles by truck\n")
            print(f"Truck 1: {truck_miles['TRUCK_1']}")
            print(f"Truck 2: {truck_miles['TRUCK_2']}")
            print(f"Truck 3: {truck_miles['TRUCK_3']}")

        print("\nSalt Lake City Delivery Service")
        print("---------------------------------")
        print("A: View Delivery Status")
        print("B: Truck mileage")
        print("Q: Quit")
        user_input = input()


# Main execution block
hash_map_1 = HashMap()
start_time = dt.datetime(2025, 6, 18, 8)
load_delivery_data("WGUPS_Package_File.csv")
address_dict, distance_between_address = load_distance_data("WGUPS_Distance_Table.csv")

delivery(TRUCK_1, start_time, address_dict, distance_between_address, truck_miles, "TRUCK_1")
delivery(TRUCK_2, start_time, address_dict, distance_between_address, truck_miles, "TRUCK_2")
delivery(TRUCK_3, start_time, address_dict, distance_between_address, truck_miles, "TRUCK_3")
package_interface()
hash_map_1.get_all_packages()
