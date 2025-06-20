#Student ID: 011383845
import csv
from datetime import datetime, timedelta
from hash_map import HashMap
from package import Package

TRUCK_1 = [4, 5, 6, 7, 8, 9, 10, 11, 12]
TRUCK_2 = [1, 3, 18, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 36, 38]
TRUCK_3 = [2, 13, 14, 15, 16, 17, 19, 20, 31, 32, 33, 34, 35, 37, 39, 40]

def load_delivery_data(file_name) -> None:
    with open(file_name) as package_file:
        delivery_data = csv.reader(package_file, delimiter=",")
        for package in delivery_data:
            package_id = int(package[0]) # cast to integer for computational use
            delivery_address = package[1]
            delivery_city = package[2]
            delivery_state = package[3]
            delivery_zip = package[4]
            delivery_deadline = package[5]
            delivery_weight = package[6]

            package = Package(package_id, delivery_address, delivery_city, delivery_state, delivery_zip, delivery_deadline, delivery_weight)
            hash_map_1.insert(package_id, package)

def load_distance_data(file_name) -> list and dict:
    #Used to store the addresses and indexes as key:value pair
    address_indices = {}
    #Used to store the distance floats
    distances_between_address = []
    with open(file_name) as distance_file:
        distance_table = csv.reader(distance_file, delimiter=",")
        for index, distance in enumerate(distance_table):
            #Addresses saved as key in dictionary
            address_indices[distance[0]] = index
            #Removes the addresses to save list of floats in a separate table
            distance.pop(0)
            distances_between_address.append(distance)

        return address_indices, distances_between_address


start_time = datetime(2025, 6, 18, 8)
def delivery(truck: list, time: object, address_dict, distance_floats):
    #Starting location will never change
    THE_HUB = 0
    min_distance = float("inf")
    current_truck_location = THE_HUB
    for package_id in truck:
        package_obj = hash_map_1.package_lookup(package_id)
        address_index = address_dict[package_obj.address]
        print(f"id {package_id}: {package_obj}") # FIX ME
        print(f"truck location: {current_truck_location}") # FIX ME

        #Distance table has empty cells. This prevents querying an empty cell
        if address_index >= current_truck_location:
            address_distance = float(distance_floats[address_index][current_truck_location])
        else:
            address_distance = float(distance_floats[current_truck_location][address_index])

            if min_distance > address_distance:
                min_distance = address_distance
                closest_package_id = package_id
                closest_address_index = address_index

    current_truck_location = closest_address_index
    print(current_truck_location)


    #print(start_time.strftime("%I:%M %p")) // FIX ME


hash_map_1 = HashMap()
load_delivery_data("WGUPS_Package_File.csv")
address_dict, distance_between_address = load_distance_data("WGUPS_Distance_Table.csv")
#print(distance_floats[2][1]) # distance between 1330 2100 S and 1060 Dalton // FIX ME


print(f"Address indices: {address_dict}\n")

delivery(TRUCK_1, start_time, address_dict, distance_between_address)
#delivery(truck_2, start_time) // FIX ME
#delivery(truck_3, start_time) // FIX ME


""" // FIX ME
delivery(truck_1)
delivery((truck_2)
delivery((truck_3)
"""






