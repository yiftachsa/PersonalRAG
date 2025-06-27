# from .app import main
#
# if __name__ == "__main__":
#     main()
# Main/main.py
import os
import sys
from typing import Optional

from menu import MenuSystem
from OOP.manager import Manager


def main():
    manager = Manager()
    menu = MenuSystem()

    while True:
        choice = menu.show_menu()

        if choice == 1:  # Initialize new version
            version_name = input("Enter version name: ")
            source_path = input("Enter source documents path: ")
            try:
                manager.init_version(version_name, source_path)
                print(f"Version {version_name} initialized successfully")
            except Exception as e:
                print(f"Error: {str(e)}")

        elif choice == 2:  # Start new conversation
            versions = manager.list_versions()  # versions is a list of dictionaries
            if not versions:
                print("No versions found. Please initialize a version first.")
                continue

            print("\nAvailable versions:")
            for i, v in enumerate(versions, 1):
                print(f"{i}. {v}")

            try:
                version_idx = int(input("\nSelect version (number): ")) - 1
                if 0 <= version_idx < len(versions):
                    version_name = versions[version_idx]["version"]
                    conv_id = manager.start_conversation(version_name)
                    print(f"Started new conversation with ID: {conv_id}")
                    chat_loop(manager)
                else:
                    print("Invalid version selection")
            except ValueError:
                print("Please enter a valid number")

        elif choice == 3:  # Update vector store
            versions = manager.list_versions()
            if not versions:
                print("No versions found.")
                continue

            print("\nAvailable versions:")
            for i, v in enumerate(versions, 1):
                print(f"{i}. {v}")

            try:
                version_idx = int(input("\nSelect version to update (number): ")) - 1
                if 0 <= version_idx < len(versions):
                    version_name = versions[version_idx]["version"]  # TODO: add ["version"]
                    manager.update_vector_store(version_name)
                    print("Vector store updated successfully")
                else:
                    print("Invalid version selection")
            except ValueError:
                print("Please enter a valid number")

        elif choice == 4:  # List conversations #TODO: add list versions
            convs = manager.list_conversations()
            if not convs:
                print("No conversations found.")
                continue

            print("\nAvailable conversations:")
            for i, v in enumerate(convs, 1):
                print(f"{i}. {v}")

        elif choice == 5:  # Continue conversation
            convs = manager.list_conversations()
            if not convs:
                print("No conversations found.")
                continue

            print("\nAvailable conversations:")
            for i, v in enumerate(convs, 1):
                print(f"{i}. {v}")

            try:
                conv_idx = int(input("\nSelect conversation (number): ")) - 1
                if 0 <= conv_idx < len(convs):
                    conv_details = convs[conv_idx]
                    conv_id = manager.continue_conversation(conv_details["version"], conv_details["conv_id"])
                    print(f"Continuing conversation with ID: {conv_id}")
                    chat_loop(manager)
                else:
                    print("Invalid conversation selection")
            except ValueError:
                print("Please enter a valid number")

        elif choice == 6:  # Exit
            print("Goodbye!")
            break


def chat_loop(manager: Manager):
    """Handle the chat interaction loop"""
    print("\n=== Chat Mode ===")
    print("Type 'exit' to end the conversation")
    print("Type 'history' to view conversation history")
    print("=" * 20)

    while True:
        try:
            user_input = input("\nYou: ").strip()

            if user_input.lower() == 'exit':
                print("Ending conversation...")
                break
            elif user_input.lower() == 'history':
                messages = manager.get_messages()
                for message in messages:
                    print(f"{message['role'].capitalize()}: {message['content']}")
                continue

            response = manager.query(user_input)
            print(f"AI: {response}")
        except Exception as e:
            print(f"Error: {e}")
