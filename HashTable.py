# Chaining hash table for holding package objects
class HashTable:
    # Initializes the hash table with the given size
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]
        self.num_items = 0

    # Modulo hash function to create an index for the given key
    def hash_function(self, key):
        return hash(key) % self.size

    # Inserts a package into the hash table
    # package_id is the key
    def insert(self, package):
        # Doubles the size of the hash table if it is full
        if self.num_items >= self.size:
            self.resize()

        # Uses hash function to compute the bucket index
        bucket = self.hash_function(package.package_id)
        bucket_list = self.table[bucket]

        # Appends the package to the appropriate bucket
        bucket_list.append(package)
        self.num_items += 1

    # Searches for and returns package with matching package_id in hash table
    # Returns None if not found
    def lookup(self, package_id):
        # Uses hash function to compute the bucket index
        bucket = self.hash_function(package_id)
        bucket_list = self.table[bucket]

        # Searches for the package in the appropriate bucket
        for package in bucket_list:
            if package.package_id == package_id:
                return package

        return None

    # Private method to double the size of the hash table
    def _resize(self):
        new_size = self.size * 2
        new_table = [[] for _ in range(new_size)]

        # Rehash existing packages and insert them into the new table
        for bucket_list in self.table:
            for package in bucket_list:
                new_bucket = self.hash_function(package.package_id) % new_size
                new_table[new_bucket].append(package)

        # Update size and replace old table with the new table
        self.size = new_size
        self.table = new_table
