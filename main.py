# Student ID: 011383845

import csv
import datetime as dt
from hash_map import HashMap
from package import Package

# Package IDs stored in manually loaded trucks
TRUCK_1 = [4, 5, 6, 7, 8, 9, 10, 11, 12]
TRUCK_2 = [1, 3, 18, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 36, 38]
TRUCK_3 = [2, 13, 14, 15, 16, 17, 19, 20, 31, 32, 33, 34, 35, 37, 39, 40]

def load_delivery_data(file_name) -> None:
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
    address_indices = {}
    distances_between_address = []
    with open(file_name) as distance_file:
        distance_table = csv.reader(distance_file, delimiter=",")
        for index, distance in enumerate(distance_table):
            address_indices[distance[0]] = index
            distance.pop(0)
            distances_between_address.append(distance)
        return address_indices, distances_between_address

truck_miles = {"TRUCK_1": 0, "TRUCK_2": 0, "TRUCK_3": 0}

def delivery(truck: list, time: object, address_dict: dict, distance_floats: list, truck_miles: dict, truck_identifier: str) -> None:
    THE_HUB = 0
    total_mileage = 0
    current_truck_location = THE_HUB
    TRUCK_SPEED = 18

    while any(hash_map_1.package_lookup(package_id).status != "Delivered" for package_id in truck):
        closest_distance = float("inf")
        closest_package_id = None
        closest_address_index = None

        for package_id in truck:
            package_obj = hash_map_1.package_lookup(package_id)
            address_index = address_dict[package_obj.address]

            if package_obj.status != "Delivered":
                if address_index >= current_truck_location:
                    address_distance = float(distance_floats[address_index][current_truck_location])
                else:
                    address_distance = float(distance_floats[current_truck_location][address_index])

                if address_distance < closest_distance:
                    closest_distance = address_distance
                    closest_package_id = package_id
                    closest_address_index = address_index

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

def get_status_at_time(package, input_time, truck_start_time, delayed_time, address_update):
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

def package_interface() -> object:
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

            wrong_address_filed = [9]
            address_update_time = "10:20 AM"
            address_update = dt.datetime.strptime(address_update_time, "%I:%M %p")

            for package in hash_map_1.get_all_packages():
                status = get_status_at_time(package, input_time, truck_start_time, delayed_time, address_update)

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

                print(f"[{truck_id}] {display_address}, {package.city}, {package.state} {package.zip} | "f"Deadline: {package.deadline} | Weight: {package.weight} lbs | Status: {status}")

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
