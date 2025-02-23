import heapq
import math

class Node:
    def __init__(self, price, bedroom, AC_NON_AC, address, deposit, fridge, oven, washing_machine, furnished, wifi,
                 name, parking, gender,latitude,longitude):
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
        self.latitude = latitude
        self.longitude = longitude

    @staticmethod
    def calculate_distance(lat1, lon1, lat2, lon2):
        """Calculate the Haversine distance between two coordinates (lat, lon)"""
        R = 6371  # Earth's radius in km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(
            dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c  # Distance in km


    def __lt__(self, other):
        return ((self.distance if self.distance is not None else float('inf')), self.price) < \
            ((other.distance if other.distance is not None else float('inf')), other.price)

    def __repr__(self):
        return f"[Name: {self.name}, Price: {self.price}, Distance: {self.distance:.2f}km]"

# MinHeap class remains the same
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

