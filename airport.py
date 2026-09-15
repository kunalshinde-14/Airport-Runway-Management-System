class Plane:
    def __init__(self, flight_no, airline, source, destination, aircraft):
        self.flight_no = flight_no
        self.airline = airline
        self.source = source
        self.destination = destination
        self.aircraft = aircraft
        self.status = "Registered"

    def display(self):
        print(f"Flight No. : {self.flight_no}")
        print(f"Airline    : {self.airline}")
        print(f"Route      : {self.source} → {self.destination}")
        print(f"Aircraft   : {self.aircraft}")
        print(f"Status     : {self.status}")


class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, plane):
        self.items.append(plane)
        print(f"{plane.flight_no} added to queue.")

    def dequeue(self):
        if len(self.items) == 0:
            print("Queue is empty.")
            return None

        plane = self.items.pop(0)
        return plane

    def display(self):
        if len(self.items) == 0:
            print("Queue is empty.")
            return

        print("\nPlanes in Queue:")

        for plane in self.items:
            print(f"{plane.flight_no} - {plane.airline}")


class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [None] * size

    def hash_function(self, flight_no):
        total = 0

        for char in flight_no:
            total += ord(char)

        return total % self.size

    def insert(self, plane):
        index = self.hash_function(plane.flight_no)
        original_index = index

        while self.table[index] is not None:

            print(
                f"Collision at index {index} "
                f"for {plane.flight_no}"
            )

            index = (index + 1) % self.size

            if index == original_index:
                print("Hash table is full.")
                return

        self.table[index] = plane

        print(
            f"{plane.flight_no} stored at index {index}"
        )

    def search(self, flight_no):
        index = self.hash_function(flight_no)
        original_index = index

        while self.table[index] is not None:

            if self.table[index].flight_no == flight_no:
                return self.table[index]

            index = (index + 1) % self.size

            if index == original_index:
                break

        return None

    def delete(self, flight_no):
        index = self.hash_function(flight_no)
        original_index = index

        while self.table[index] is not None:

            if self.table[index].flight_no == flight_no:

                self.table[index] = None

                # Reinsert following collided elements
                # so that searching still works.
                next_index = (index + 1) % self.size

                while self.table[next_index] is not None:

                    plane = self.table[next_index]
                    self.table[next_index] = None
                    self.insert(plane)

                    next_index = (next_index + 1) % self.size

                return True

            index = (index + 1) % self.size

            if index == original_index:
                break

        return False

    def display(self):
        print("\nFlight Hash Table:")

        for i in range(self.size):

            if self.table[i] is None:
                print(f"Index {i}: Empty")

            else:
                print(
                    f"Index {i}: "
                    f"{self.table[i].flight_no}"
                )

class Stack:
    def __init__(self):
        self.items = []

    def push(self, plane):
        self.items.append(plane)

    def pop(self):
        if len(self.items) == 0:
            return None

        return self.items.pop()

    def display(self):
        if len(self.items) == 0:
            print("History is empty.")
            return

        for plane in reversed(self.items):
            print(f"{plane.flight_no} - {plane.airline}")