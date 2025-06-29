from typing import List, Dict, Optional, Callable, Any
from dataclasses import dataclass
import os
from pprint import pprint


@dataclass
class MenuItem:
    number: int
    text: str


class MenuSystem:
    def __init__(self):
        self.current_version = None
        self.current_conv_id = None
        self.is_running = True

    def show_menu(self) -> int:
        """Display the main menu and return user's choice"""
        self._clear_screen()
        print("\n=== Personal RAG System ===")

        menu_items = [
            MenuItem(1, "Initialize new version"),
            MenuItem(2, "Start new conversation"),
            MenuItem(3, "Update vector store"),
            MenuItem(4, "List conversations"),
            MenuItem(5, "Continue conversation"),
            MenuItem(6, "Exit")
        ]

        # Display menu
        for item in menu_items:
            print(f"{item.number}. {item.text}")

        # Get user choice
        try:
            choice = int(input("\nEnter your choice (1-6): "))
            if 1 <= choice <= 6:
                return choice
            print("\nPlease enter a number between 1 and 6.")
            input("Press Enter to continue...")
            return 0
        except ValueError:
            print("\nPlease enter a valid number.")
            input("Press Enter to continue...")
            return 0

    def get_version_choice(self, versions: List[Dict[str, str]], prompt: str) -> int:
        """Display versions and get user's choice"""
        if not versions:
            print("No versions available.")
            input("Press Enter to continue...")
            return -1

        print(f"\n{prompt}:")
        for i, version in enumerate(versions, 1):
            print(f"{i}. {version}")

        try:
            choice = int(input("\nEnter number (or 0 to cancel): "))
            if 0 <= choice <= len(versions):
                return choice - 1  # Return index or -1 for cancel
            return -1
        except ValueError:
            return -1

    def show_convs(self, conversations: List[Dict[str, str]]):
        """Display all conversations to the user"""
        print(f"\n=== All Conversations ===")
        for i, conv in enumerate(conversations, 1):
            # print(f"{i}: {conv})")
            pprint(f"{i}: {conv}")

        input("Press Enter to continue...")

    def get_conversation_choice(self, conversations: List[Dict[str, str]]) -> int:
        """Display conversations and get user's choice"""
        if not conversations:
            print("No conversations available.")
            input("Press Enter to continue...")
            return -1

        print("\nAvailable conversations:")
        for i, conv in enumerate(conversations, 1):
            pprint(f"{i}: {conv}")
            # print(f"{i}: {conv})")

        try:
            choice = int(input("\nEnter number (or 0 to cancel): "))
            if 0 <= choice <= len(conversations):
                return choice - 1  # Return index or -1 for cancel
            return -1
        except ValueError:
            return -1

    def get_input(self, prompt: str, required: bool = True) -> str:
        """Get input from user with optional validation"""
        while True:
            value = input(prompt).strip()
            if not required or value:
                return value
            print("This field is required.")

    def _clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def show_message(self, message: str):
        """Display a message to the user"""
        print(f"\n{message}")
        input("Press Enter to continue...")

    def chat_loop(self, query_callback, history_callback):
        """Handle the chat interaction loop
        
            :param query_callback: A function that takes a user message and returns the AI's response
            :param history_callback:
        """
        print("\n=== Chat Mode ===")
        print("Type 'exit' to end the conversation")
        print("Type 'history' to view conversation history")
        print("Type 'back' to return to main menu")
        print("=" * 20)

        while True:
            try:
                user_input = input("\nYou: ").strip()

                if user_input.lower() == 'exit':
                    print("Ending conversation...")
                    break
                elif user_input.lower() == 'back':
                    return
                elif user_input.lower() == 'history':
                    message_history = history_callback()
                    for message in message_history:
                        print(f"{message['role'].capitalize()}: {message['content']}")
                    continue

                response = query_callback(user_input)
                print(f"AI: {response}")
            except Exception as e:
                print(f"Error: {e}")

    def _handle_exit(self):
        """Handle application exit"""
        print("\nThank you for using Personal RAG System. Goodbye!")
        self.is_running = False
