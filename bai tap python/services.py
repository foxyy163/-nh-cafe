import random
from models import User, Admin, Room, Booking, BookingStatus

class AuthService:
    def __init__(self):
        self.users = []

    def register(self, username, password, email):
        for u in self.users:
            if u.username == username:
                return None
        user = User(len(self.users) + 1, username, password, email)
        self.users.append(user)
        return user

    def login(self, username, password):
        for u in self.users:
            if u.username == username and u.password == password:
                return u
        return None

    def reset_password(self, email):
        for u in self.users:
            if u.email == email and u.role == "customer":
                code = random.randint(100000, 999999)
                print(f"[Mock Email] Reset code sent to {email}: {code}")
                return True
        return False

class RoomService:
    def __init__(self):
        self.rooms = []

    def add_room(self, room):
        self.rooms.append(room)

    def get_available_rooms(self):
        return [r for r in self.rooms if r.status == "Available"]

    def search_room(self, keyword):
        return [r for r in self.rooms if keyword.lower() in r.room_type.lower()]

class BookingService:
    def __init__(self):
        self.bookings = []

    def create_booking(self, user_id):
        booking = Booking(len(self.bookings) + 1, user_id)
        self.bookings.append(booking)
        return booking

    def get_user_bookings(self, user_id):
        return [b for b in self.bookings if b.user_id == user_id]

class PaymentService:
    def checkout(self, booking):
        print("\n--- CHECKOUT ---")
        total = booking.calculate_total()
        print(f"Total amount: {total}")

        choice = input("Confirm payment? (y/n): ")
        if choice.lower() == "y":
            booking.status = BookingStatus.CONFIRMED
            print("Payment successful!")
        else:
            booking.status = BookingStatus.PAYMENT_FAILED
            print("Payment failed!")
