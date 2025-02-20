import heapq
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

class Node:
    def __init__(self, price, bedroom, AC_NON_AC, address, deposit, fridge, oven, washing_machine, furinshed, wifi, name,
                 parking, gender):
        self.name = name
        self.price = price
        self.AC_NON_AC = AC_NON_AC  # True for AC, False for non-AC
        self.distance = None
        self.bedroom = bedroom
        self.address = address
        self.deposit = deposit
        self.fridge = fridge
        self.oven = oven
        self.washing_machine = washing_machine
        self.furinshed = furinshed
        self.wifi = wifi
        self.parking = parking
        self.gender = gender
        
    def calculate_distance(self, other_address):
        geolocator = Nominatim(user_agent="your_app_name")
        location1 = geolocator.geocode(self.address)
        location2 = geolocator.geocode(other_address)
        if location1 and location2:
            self.distance = geodesic(location1.point, location2.point).kilometers
        else:
            self.distance = None


    def __lt__(self, other):
        return (self.price, self.distance) < (other.price, other.distance)

    def __repr__(self):
        return f"[Name: {self.name}]"


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
    node1 = Node(500, 2, "Hostel A", "123 Street", 100, True, False, True, True, True, False, True, 'Male')
    node2 = Node(700, 5, "Hostel B", "456 Avenue", 200, True, True, True, True, True, "Female",True,'Male')

    node1.calculate_distance("789 Road")
    print(round(node1.distance,2))  # Output: Distance in miles between node1 and "789 Road"

    node2.calculate_distance("123 Street")
    print(node2.distance)  # Output: Distance in miles between node2 and "123 Street"
    # heap = MinHeap()
    # heap.push(Node(500, 2, "Hostel A", 1, "123 Street", 100, True, False, True, True, False, "Male"))
    # heap.push(Node(700, 5, "Hostel B", 2, "456 Avenue", 200, True, True, True, True, True, "Female"))
    # heap.push(Node(600, 3, "Hostel C", 1, "789 Road", 150, False, True, False, True, False, "Male"))
    #
    # print("Heap:", heap)
    #
    # print("Popping elements in price range 500-650:", heap.pop_in_price_range(500, 650))
    # print("Heap after popping:", heap)
