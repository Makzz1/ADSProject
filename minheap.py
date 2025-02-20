import heapq
import time
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

# Cache to store latitude & longitude (reducing API calls)
cached_locations = {}


class Node:
    def __init__(self, price, bedroom, AC_NON_AC, address, deposit, fridge, oven, washing_machine, furnished, wifi,
                 name,
                 parking, gender):
        self.name = name
        self.price = price
        self.AC_NON_AC = AC_NON_AC
        self.distance = None
        self.bedroom = bedroom
        self.address = address
        self.deposit = deposit
        self.fridge = fridge
        self.oven = oven
        self.washing_machine = washing_machine
        self.furnished = furnished
        self.wifi = wifi
        self.parking = parking
        self.gender = gender

    def get_location(self, address):
        """Get latitude & longitude with caching and retry mechanism."""
        if address in cached_locations:
            return cached_locations[address]

        geolocator = Nominatim(user_agent="your_app_name", timeout=10)  # Increased timeout
        retries = 3  # Retry up to 3 times if failure
        for attempt in range(retries):
            try:
                location = geolocator.geocode(address)
                if location:
                    cached_locations[address] = (location.latitude, location.longitude)
                    return cached_locations[address]
            except Exception as e:
                print(f"Attempt {attempt + 1} failed for {address}: {e}")
                time.sleep(2)  # Wait 2 seconds before retrying

        return None  # If all attempts fail

    def calculate_distance(self, other_address):
        """Calculate distance using cached coordinates to avoid timeout issues."""
        location1 = self.get_location(self.address)
        location2 = self.get_location(other_address)

        if location1 and location2:
            self.distance = geodesic(location1, location2).kilometers
        else:
            self.distance = None  # Set None if geocoding fails

    def __lt__(self, other):
        return (self.price, self.distance) < (other.price, other.distance)

    def __repr__(self):
        return f"[Name: {self.name}, Price: {self.price}, Distance: {self.distance} km]"


class MinHeap:
    def __init__(self):
        self.heap = []

    def push(self, node):
        heapq.heappush(self.heap, node)

    def pop(self):
        return heapq.heappop(self.heap) if self.heap else None

    def peek(self):
        return self.heap[0] if self.heap else None

    def is_empty(self):
        return len(self.heap) == 0

    def pop_in_price_range(self, min_price, max_price):
        temp_heap = []
        result = []
        while self.heap:
            node = heapq.heappop(self.heap)
            if min_price <= node.price <= max_price:
                result.append(node)
            else:
                temp_heap.append(node)
        for node in temp_heap:
            heapq.heappush(self.heap, node)
        return result

    def __repr__(self):
        return str(self.heap)


# Example usage
if __name__ == '__main__':
    node1 = Node(500, 2, "AC", "Chennai, Tamil Nadu, India", 100, True, False, True, True, True, "Hostel A", True,
                 "Male")
    node2 = Node(700, 5, "Non-AC", "Bangalore, Karnataka, India", 200, True, True, True, True, True, "Hostel B", True,
                 "Male")

    node1.calculate_distance("Mumbai, Maharashtra, India")
    print(f"Distance (Node1 to Mumbai): {round(node1.distance, 2)} km")

    node2.calculate_distance("Chennai, Tamil Nadu, India")
    print(f"Distance (Node2 to Chennai): {round(node2.distance, 2)} km")
