class Package:
    # Initialize the Package object with its attributes
    def __init__(self, package_id, address, city, zip_code, delivery_deadline, weight, status):
        self.package_id = package_id  # Unique identifier for the package
        self.address = address  # Street address of where the package is to be delivered
        self.city = city  # City where the package is to be delivered
        self.zip_code = zip_code  # Zip code where the package is to be delivered
        self.delivery_deadline = delivery_deadline  # Deadline of when the package is to be delivered
        self.weight = weight  # Weight of the package in kg
        self.status = status  # Status of the package (at hub, en route, delivered)
        self.departure_time = None  # Time package left the hub
        self.delivery_time = None  # Time package was delivered
        self.truck_id = None  # ID of the truck the package was loaded onto

    # Update status of package based off a given time
    def update_status(self, timestamp):
        # Package is at hub if the timestamp is before the departure time
        if timestamp < self.departure_time:
            self.status = 'At Hub'
        # Package is en route if timestamp is after departure time but before the delivery time
        elif timestamp < self.delivery_time:
            self.status = f'En Route by Truck {self.truck_id} @ {self.departure_time}'
        # Else, the package is delivered
        else:
            self.status = f'Delivered by Truck {self.truck_id} @ {self.delivery_time}'

    # Returns string of package's attributes
    def __str__(self):
        return (f"ID: {self.package_id:<2} | ADDRESS: {self.address:<39} | CITY: {self.city:<17} | "
                f"STATE: UT | ZIP: {self.zip_code:<5} | DEADLINE: {self.delivery_deadline:<10} | "
                f"WEIGHT (in kilos): {self.weight:<2} | STATUS: {self.status}")
