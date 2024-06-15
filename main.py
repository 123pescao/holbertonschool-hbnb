#!/usr/bin/python3
from model.data_manager import DataManager
from model.user import User
from model.place import Place

def main():
    data_manager = DataManager()

    # Create and save a new user
    user = User(email="test@example.com", first_name="John", last_name="Doe")
    data_manager.save(user)

    # Retrieve the user
    retrieved_user = data_manager.get(user.id, 'User')
    print("Retrieved User:", retrieved_user)

    # Update the user
    user.first_name = "Jane"
    data_manager.update(user)

    # Delete the user
    data_manager.delete(user.id, 'User')

if __name__ == "__main__":
    main()
