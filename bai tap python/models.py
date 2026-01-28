from enum import Enum
from datetime import datetime

class User:
    def __init__(self, user_id, username, password, email="", role="customer"):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.email = email
        self.role = role

    def get_role(self):
        return self.role


class Admin(User):
    def __init__(self, user_id, username, password):
        super().__init__(user_id, username, password, email="", role="admin")

class Room:
    def __init__(self, room_id, room_type, price, description, status="Available", image_link=""):
        self.room_id = room_id
        self.room_type = room_type
        self.price = price
        self.description = description
        self.status = status
        self.image_link = image_link

    def show_info(self):
        print(f"Room ID: {self.room_id}")
        print(f"Type: {self.room_type}")
        print(f"Price per night: {self.price}")
        print(f"Status: {self.status}")
        print(f"Image link: {self.image_link}")
        print("-" * 30)

class BookingStatus(Enum):
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    PAYMENT_FAILED = "Payment Failed"


class Booking:
    def __init__(self, booking_id, user_id):
        self.booking_id = booking_id
        self.user_id = user_id
        self.rooms = []
        self.nights = 1
        self.total_amount = 0
        self.status = BookingStatus.PENDING
        self.created_at = datetime.now()

    def add_room(self, room):
        self.rooms.append(room)

    def calculate_total(self):
        self.total_amount = sum(r.price for r in self.rooms) * self.nights
        return self.total_amount
