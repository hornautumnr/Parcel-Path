ParcelPath 📦
----------------
ParcelPath simulates a real-world package delivery scenario, using efficient algorithms and data structures to organize,
schedule, and track package deliveries. The goal was to minimize mileage while maintaining accurate package tracking 
from hub departure to final delivery.

Project Goals
-----------------
1. Deliver all 40 packages with a total mileage under 140 miles.
2. Provide accurate and real-time tracking of each package's status.
3. Use efficient data structures for package management and quick lookups.

Features
----------
- **Optimized Route Planning:** Implements a nearest-neighbor algorithm to dynamically select the closest delivery 
destination, ensuring minimal mileage.
- **Real-Time Package Tracking:** Updates and logs package statuses as they are delivered.
- **Custom Data Structures:** Uses a chaining hash table (HashTable) to efficiently store and retrieve package information.
- **Interactive Console Menu:**
  - View real-time truck logs and total mileage.
  - Query individual or all package statuses at a specified time.

Technical Details 
--------------------
### Data Structures
- **HashTable:** A chaining hash table that stores and retrieves package data, allowing efficient lookups and storage.
- **2D Array:** Holds distance data between locations for quick access when calculating optimal routes.

## Algorithm Design
- **Nearest-Neighbor Algorithm:** Calculates the shortest path to the next package destination, optimizing delivery
mileage to achieve a total of 72.7 miles.
- **File I/O and Persistence:** Reads data from CSV files (packages, distances, addresses) and write delivery updates to
maintain consistency across sessions.

Technologies and Skills
--------------------------
- **Programming Language:** Python
- **Core Libraries:** `csv', 'datetime`
- **Data Structures:** Hash table, 2D arrays, and lists
- **Algorithmic Skills:** Route optimization and dynamic data management
- **File I/O and Data Persistence:** Imports and exports data using CSV for persistent storage.

Results
----------
ParcelPath successfully delivers all packages with a total distance of **72.7 miles**, well under the 140-mile goal.
This achievement showcases the effectiveness of the nearest-neighbor alogrithm in real-world routing challenges.