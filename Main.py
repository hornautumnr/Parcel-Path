# Autumn Horn

from Package import Package
from HashTable import HashTable
from Truck import Truck
import csv
import datetime

packageHash = HashTable(40)  # Hash table for storing packages

# Load hash table with packages from package csv file
with open('PackageCSV.csv', 'r') as packageCSV:
    packageReader = csv.reader(packageCSV)
    for row in packageReader:
        package = Package(
            package_id=int(row[0]),
            address=row[1],
            city=row[2],
            zip_code=row[4],
            delivery_deadline=row[5],
            weight=row[6],
            status='at the hub'
        )

        packageHash.insert(package)

# 27 x 27 2D array for storing distance data
distanceData = [[0 for _ in range(27)] for _ in range(27)]

# Load array with distance data from csv file
with open('DistanceCSV.csv', 'r') as distanceCSV:
    distanceReader = csv.reader(distanceCSV)
    for i, row in enumerate(distanceReader):
        for j, value in enumerate(row):
            if value:
                distanceData[i][j] = float(value)

# List for storing addresses
addressList = []

# Load list with addresses from csv file
with open('AddressCSV.csv', 'r') as addressCSV:
    addressReader = csv.reader(addressCSV)
    for row in addressReader:
        addressList.append(row[0])

# Hub address
hub = addressList[0]

# Initialize and load trucks, set departure times, and assign drivers
# 3 trucks, 2 drivers (Frank and Bob)
truck_1 = Truck(
    1,
    [1, 12, 13, 14, 15, 16, 19, 20, 21, 27, 30, 34, 35, 37, 39],
    hub,
    0,
    datetime.timedelta(hours=int(8), minutes=int(0), seconds=int(0)),
    'Frank')

# Truck 2 leaves last at 10:30AM (after Bob returns with Truck 3)
truck_2 = Truck(
    2,
    [3, 5, 8, 9, 10, 11, 18, 23, 36, 38],
    hub,
    0,
    datetime.timedelta(hours=int(10), minutes=int(30), seconds=int(0)),
    'Bob')

truck_3 = Truck(
    3,
    [2, 4, 6, 7, 17, 22, 24, 25, 26, 28, 29, 31, 32, 33, 40],
    hub,
    0,
    datetime.timedelta(hours=int(9), minutes=int(5), seconds=int(0)),
    'Bob')


# Returns index of address in addressList
def address_lookup(address):
    return addressList.index(address)


# Returns distance between two addresses using distance data array
def distance_between(address1, address2):
    distance = distanceData[address_lookup(address1)][address_lookup(address2)]
    if distance == 0:
        distance = distanceData[address_lookup(address2)][address_lookup(address1)]
    return distance


# Uses nearest neighbor algorithm to find the nearest package to be delivered from the current address
# Returns a tuple containing the nearest package object and the distance to it
def find_next_package(from_address, packages):
    min_distance = 50  # Initial maximum distance threshold
    next_package = None  # Variable to store the nearest package

    # Iterate over all packages to find the nearest one
    for p in packages:
        package_obj = packageHash.lookup(p)  # Lookup package in hashtable by its package ID
        package_address = package_obj.address  # Get the package's address
        package_distance = distance_between(from_address, package_address)  # Calculate distance to the package address

        # Update the nearest package if the current one is closer or equally close
        if package_distance <= min_distance:
            min_distance = package_distance
            next_package = package_obj

    return next_package, min_distance


# Calculates the delivery time of a package based on a truck's departure time, mileage, and travel speed
# Trucks travel 18 mph
def time_delivered(depart_time, mileage):
    # Calculate hours, minutes, and seconds to deliver the package
    hours_to_deliver = mileage / 18
    minutes_to_deliver = (hours_to_deliver - int(hours_to_deliver)) * 60
    seconds_to_deliver = round((minutes_to_deliver - int(minutes_to_deliver)) * 60)

    # Calculate delivery time by adding the travel time to the truck's departure time
    delivery_time = depart_time + datetime.timedelta(hours=int(hours_to_deliver), minutes=int(minutes_to_deliver),
                                                     seconds=int(seconds_to_deliver))

    return delivery_time


# Deliver packages assigned to a truck
def deliver_packages(truck):
    # Correct address and zip code of package #9 for truck #2
    if truck.truck_id == 2:
        package_to_update = packageHash.lookup(9)
        package_to_update.address='410 S State St'
        package_to_update.zip_code='84111'

    # Update statuses of all packages to 'En route' and assign them to the truck
    for p in truck.packages:
        package_obj = packageHash.lookup(p)
        package_obj.truck_id = truck.truck_id
        package_obj.status = f'En route by Truck {truck.truck_id} @ {truck.depart_time}'
        package_obj.departure_time = truck.depart_time

    # While there are still packages to deliver
    while len(truck.packages) > 0:
        # Find the closest package address to deliver and the travel distance to it
        current_package, travel_distance = find_next_package(truck.current_address, truck.packages)

        # Update the truck's mileage and current address, then remove the package
        truck.mileage += travel_distance
        truck.current_address = current_package.address
        truck.packages.remove(current_package.package_id)

        # Add package to the truck's list of delivered packages
        truck.delivered_packages.append(current_package.package_id)

        # Update the package's status and delivery time
        delivery_time = time_delivered(truck.depart_time, truck.mileage)  # Calculate delivery time
        current_package.delivery_time = delivery_time
        current_package.status=f'Delivered by Truck {truck.truck_id} @ {delivery_time}'  # Update package status


# Return truck to hub address
# Updates truck's mileage with the distance from its current location to the hub
def return_to_hub(truck):
    distance_from_hub = distance_between(hub, truck.current_address)
    truck.current_address = hub
    truck.mileage += distance_from_hub


# Deliver packages on truck #1
deliver_packages(truck_1)

# Find truck #1's delivery completion time based on its departure time and ending mileage
truck_1.completion_time = time_delivered(truck_1.depart_time, truck_1.mileage)

# Deliver packages on truck #3
deliver_packages(truck_3)

# Find truck #3's delivery completion time
truck_3.completion_time = time_delivered(truck_3.depart_time, truck_3.mileage)

# Return truck #3 to hub (will update its mileage)
return_to_hub(truck_3)

# Find truck #3's return time using the new mileage
truck_3.return_time = time_delivered(truck_3.depart_time, truck_3.mileage)

# Deliver package on truck #2
deliver_packages(truck_2)

# Find truck #2's completion time
truck_2.completion_time = time_delivered(truck_2.depart_time, truck_2.mileage)

# Add up final mileages of each truck to calculate today's total mileage
total_mileage = truck_1.mileage + truck_2.mileage + truck_3.mileage


# Display Main menu
def display_main_menu():
    print("\n\n--------------Welcome to ParcelPath!--------------\n\n"
          "Please select an option from the menu below:\n\n"
          "1. View Today's Truck Logs \n"
          "2. View Today's Mileage \n"
          "3. Get a Single Package Status at a Given Time \n"
          "4. Get All Package Statuses at a Given Time \n"
          "5. Exit the Program\n")

    while True:
        user_choice = input('Enter Number: ')

        # Handle the user's menu choice
        if user_choice == '1':
            display_truck_logs()
            break
        elif user_choice == '2':
            display_mileage()
        elif user_choice == '3':
            display_single_package()
        elif user_choice == '4':
            display_all_packages()
        elif user_choice == '5':
            print("\nGoodbye!")
            exit()
        else:
            # Handle invalid input
            print("\n--Sorry, we didn't catch that. Please make sure you are entering a number form the menu above.--\n")


# Display Today's Truck Logs
def display_truck_logs():
    print("\n-------------------Truck Logs-------------------\n\n"
          f"{truck_1}\n"
          f"_______________________________________________\n"
          f"{truck_2}\n"
          f"_______________________________________________\n"
          f"{truck_3}\n")

    while True:
        user_input = input("Type '1' to return to main menu: ")

        # Handle user input to return to the main menu
        if user_input == '1':
            display_main_menu()
            break
        else:
            # Handle invalid input
            print("\n--Sorry, we didn't catch that. Please check your input and try again.--\n")


# Display Today's Mileage Data
def display_mileage():
    print("\n-----------------Today's Mileage-----------------\n\n"
          f"Truck 1: {truck_1.mileage} mi\n"
          f"Truck 2: {truck_2.mileage} mi\n"
          f"Truck 3: {truck_3.mileage} mi\n"
          f"***Total: {total_mileage} mi***\n")

    while True:
        user_input = input("Type '1' to return to main menu: ")

        # Handle user input to return to the main menu
        if user_input == '1':
            display_main_menu()
            break
        else:
            # Handle invalid input
            print("\n--Sorry, we didn't catch that. Please check your input and try again.--\n")


# Update package #9's address based off a given time
# Package #9's address and zip code are corrected at 10:20AM
def update_package_9(timestamp):
    package9 = packageHash.lookup(9)
    # If before 10:20
    if timestamp < datetime.timedelta(hours=int(10), minutes=int(20), seconds=int(0)):
        package9.address='300 State St'
        package9.zip='84103'
    # Else (if 10:20 or later)
    else:
        package9.address='410 S State St'
        package9.zip='84111'


# Display a single package's status at a given time
def display_single_package():
    while True:
        # Prompt user for the package ID
        package_id = input("\nPlease enter the numeric ID of the package you would like to view: ")

        try:
            package_id = int(package_id)  # Convert input to integer
        except ValueError:
            # Handles invalid input (not a number)
            print("\n--Invalid input. Please enter a numeric package ID.--")
            continue

        # Lookup the package object using the package ID
        package_obj = packageHash.lookup(int(package_id))
        if package_obj is not None:
            break  # Exit loop if package is found
        else:
            # If package not found, prompt user to try again
            print(f"\n--Sorry, Package {package_id} does not exist. Please check your input and try again.--")
    while True:
        # Prompt user for the time to view the package status
        time_input = input(f"Please enter the time (hh:mm) you would like view Package {package_id}: ")

        try:
            # Parse the inputted time
            hours, minutes = map(int, time_input.split(':'))

            # Validate the inputted time
            if 0 <= hours < 24 and 0 <= minutes < 60:
                timestamp = datetime.timedelta(hours=hours, minutes=minutes)
                break  # Exit loop if time is valid
            else:
                # If time invalid, prompt user to try again
                print(
                    "\n--Invalid time. Please make sure hours are between 0 and 23 and minutes are between 0 and "
                    "59.--\n")

        except ValueError:
            # Handles invalid input
            print('\n--Invalid Format. Please make sure your time is in the format hh:mm.--\n')

    # If package #9, update its address based on the given time
    if package_id == 9:
        update_package_9(timestamp)

    # Update the package status at the given time
    package_obj.update_status(timestamp)

    # Display the package status at the given time
    print(f"\n***Package {package_id} at {timestamp}***\n")
    package_str = str(package_obj)
    for attribute in package_str.split('|'):
        print(attribute.strip())

    while True:
        user_input = input("\nType '1' to return to main menu: ")

        # Handle user input to return to the main menu
        if user_input == '1':
            display_main_menu()
            break
        else:
            # Handles invalid input
            print("\n--Sorry, we didn't catch that. Please check your input and try again.--")


# Display all packages at a given time
def display_all_packages():
    while True:
        # Prompt user for the time they would like to view the packages
        time_input = input(f"\nPlease enter the time (hh:mm) you would like view today's packages: ")

        try:
            # Parse the inputted time
            hours, minutes = map(int, time_input.split(':'))

            # Validate the inputted time
            if 0 <= hours < 24 and 0 <= minutes < 60:
                timestamp = datetime.timedelta(hours=hours, minutes=minutes)
                break  # Exit loop if time is valid
            else:
                # If time is invalid, prompt user to try again
                print(
                    "\n--Invalid time. Please make sure hours are between 0 and 23 and minutes are between 0 and "
                    "59.--")

        except ValueError:
            # Handles invalid input
            print('\n--Invalid Format. Please make sure your time is in the format hh:mm.--')

    # Update package 9's address based on chosen time
    update_package_9(timestamp)

    print(f"\n-----------Today's Packages @ {timestamp}-----------\n")

    # Update status of all packages in hash table for inputted time and print to screen
    for package_id in range(1, 41):
        package = packageHash.lookup(package_id)
        package.update_status(timestamp)
        print(package)

    while True:
        user_input = input("\nType '1' to return to main menu: ")

        # Handles user input to return to the main menu
        if user_input == '1':
            display_main_menu()
            break
        else:
            # Handles invalid input
            print("\n--Sorry, we didn't catch that. Please check your input and try again.--")


# Display main menu
display_main_menu()
