import datetime


class Truck:
    # Initialize the Truck object with its attributes
    def __init__(self, truck_id, packages, current_address, mileage, depart_time, driver):
        self.truck_id = truck_id  # Unique identifier for the truck
        self.packages = packages  # List of undelivered packages on truck
        self.current_address = current_address  # Current location of truck
        self.mileage = mileage  # Total mileage of truck
        self.depart_time = depart_time  # Time truck leaves the hub
        self.driver = driver  # Driver of the truck
        self.completion_time = None  # Time truck completed deliveries
        self.return_time = None  # Time truck returned to the hub
        self.delivered_packages = []  # List of packages this truck has delivered

    # Returns a string representation of this truck's attributes
    def __str__(self):
        return (f"***Truck {self.truck_id}***\n"
                f"     Driver: {self.driver}\n"
                f"     Packages Delivered: {len(self.delivered_packages)}\n"
                f"     Packages Left: {len(self.packages)}\n"
                f"     Left Hub: {self.depart_time}\n"
                f"     Completed Deliveries: {self.completion_time if self.completion_time else 'N/A'}\n"
                f"     Returned To Hub: {self.return_time if self.return_time else 'N/A'}\n"
                f"     Miles Travelled: {self.mileage}\n" 
                f"     Current Address: {self.current_address}")
