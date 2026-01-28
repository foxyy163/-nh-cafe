from models import Admin, Room
from services import AuthService, RoomService, BookingService, PaymentService

auth_service = AuthService()
room_service = RoomService()
booking_service = BookingService()
payment_service = PaymentService()
admin = Admin(0, "admin", "123456")
auth_service.users.append(admin)

def user_menu(user):
    booking = None

    while True:
        print("\n--- USER MENU ---")
        print("1. Book room")
        print("2. View my bookings")
        print("3. Checkout")
        print("0. Logout")

        choice = input("Choose: ")

        if choice == "1":
            if not booking:
                booking = booking_service.create_booking(user.user_id)

            for r in room_service.get_available_rooms():
                r.show_info()

            room_id = int(input("Enter room ID: "))
            nights = int(input("Number of nights: "))
            booking.nights = nights

            for r in room_service.rooms:
                if r.room_id == room_id and r.status == "Available":
                    booking.add_room(r)
                    r.status = "Booked"
                    print("Room added to booking")
                    break

        elif choice == "2":
            for b in booking_service.get_user_bookings(user.user_id):
                print(f"Booking {b.booking_id} - Status: {b.status.value}")

        elif choice == "3":
            if booking:
                payment_service.checkout(booking)

        elif choice == "0":
            break

def admin_menu():
    while True:
        print("\n--- ADMIN MENU ---")
        print("1. Add room")
        print("2. Edit room")
        print("3. Delete room")
        print("4. View all bookings")
        print("0. Logout")

        choice = input("Choose: ")

        if choice == "1":
            rid = int(input("Room ID: "))
            rtype = input("Type: ")
            price = float(input("Price per night: "))
            desc = input("Description: ")
            img = input("Image link: ")

            room_service.add_room(
                Room(rid, rtype, price, desc, "Available", img)
            )
            print("Room added successfully!")

        elif choice == "2":
            rid = int(input("Room ID to edit: "))
            for r in room_service.rooms:
                if r.room_id == rid:
                    r.price = float(input("New price: "))
                    r.status = input("New status (Available / Booked): ")
                    print("Room updated successfully!")
                    break
            else:
                print("Room not found!")

        elif choice == "3":
            rid = int(input("Room ID to delete: "))
            for r in room_service.rooms:
                if r.room_id == rid:
                    room_service.rooms.remove(r)
                    print("Room deleted successfully!")
                    break
            else:
                print("Room not found!")

        elif choice == "4":
            if not booking_service.bookings:
                print("No bookings yet.")
            for b in booking_service.bookings:
                print(f"Booking {b.booking_id} | User {b.user_id} | {b.status.value}")

        elif choice == "0":
            break

def main():
    while True:
        print("\n=== HOTEL BOOKING SYSTEM ===")
        print("1. View available rooms")
        print("2. Search rooms")
        print("3. Register")
        print("4. Login")
        print("0. Exit")

        choice = input("Choose: ")

        if choice == "1":
            rooms = room_service.get_available_rooms()
            if not rooms:
                print("No available rooms.")
            for r in rooms:
                r.show_info()

        elif choice == "2":
            keyword = input("Enter room type keyword: ")
            results = room_service.search_room(keyword)
            if not results:
                print("No matching rooms.")
            for r in results:
                r.show_info()

        elif choice == "3":
            user = auth_service.register(
                input("Username: "),
                input("Password: "),
                input("Email: ")
            )
            print("Register success!" if user else "Username already exists!")

        elif choice == "4":
            user = auth_service.login(
                input("Username: "),
                input("Password: ")
            )

            if not user:
                print("Login failed!")
                print("Forgot password? (customer only)")
                email = input("Enter email or press Enter to skip: ")
                if email:
                    auth_service.reset_password(email)

            elif user.get_role() == "admin":
                admin_menu()
            else:
                user_menu(user)

        elif choice == "0":
            break


if __name__ == "__main__":
    main()
