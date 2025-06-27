from typing import List, Dict, Optional, Tuple, Callable, Any
from dataclasses import dataclass
import os
from pathlib import Path


@dataclass
class MenuItem:
    number: int
    text: str
    handler: Callable[[], Any]
    requires_auth: bool = False


class MenuSystem:
    def __init__(self, rag_app: 'PersonalRAG'):
        self.rag_app = rag_app
        self.current_version = None
        self.current_conv_id = None
        self.is_running = True

    def show_menu(self):
        """Display the main menu and handle user input"""
        while self.is_running:
            self._clear_screen()
            print("\n=== Personal RAG System ===")

            # Main menu items
            menu_items = [
                MenuItem(1, "Initialize new version", self._handle_init_version),
                MenuItem(2, "Start new conversation", self._handle_new_conversation),
                MenuItem(3, "Update vector store", self._handle_update_vector_store),
                MenuItem(4, "List conversations", self._handle_list_conversations),
                MenuItem(5, "Continue conversation", self._handle_continue_conversation),
                MenuItem(6, "Exit", self._handle_exit)
            ]

            # Display menu
            for item in menu_items:
                print(f"{item.number}. {item.text}")

            # Get user choice
            try:
                choice = int(input("\nEnter your choice (1-6): "))
                selected = next((item for item in menu_items if item.number == choice), None)

                if selected:
                    selected.handler()
                else:
                    print("\nInvalid choice. Please try again.")
                    input("Press Enter to continue...")

            except ValueError:
                print("\nPlease enter a valid number.")
                input("Press Enter to continue...")

    def _clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def _select_version(self, prompt: str = "Select version") -> Optional[str]:
        """Helper to select a version from available versions"""
        versions = [v["version"] for v in self.rag_app.conv_manager.list_versions()]

        if not versions:
            print("No versions available. Please initialize a version first.")
            input("Press Enter to continue...")
            return None

        print(f"\n{prompt}:")
        for i, version in enumerate(versions, 1):
            print(f"{i}. {version}")

        try:
            choice = int(input("\nEnter number (or 0 to cancel): "))
            if 1 <= choice <= len(versions):
                return versions[choice - 1]
            return None
        except (ValueError, IndexError):
            return None

    def _select_conversation(self, version: str) -> Optional[str]:
        """Helper to select a conversation from a version"""
        conversations = self.rag_app.conv_manager.list_conversations(version)

        if not conversations:
            print("No conversations found for this version.")
            input("Press Enter to continue...")
            return None

        print("\nAvailable conversations:")
        for i, conv in enumerate(conversations, 1):
            print(f"{i}. {conv['description']} ({conv['id'][:8]}...)")

        try:
            choice = int(input("\nEnter number (or 0 to cancel): "))
            if 1 <= choice <= len(conversations):
                return conversations[choice - 1]['id']
            return None
        except (ValueError, IndexError):
            return None

    def _handle_init_version(self):
        """Handle version initialization"""
        print("\n=== Initialize New Version ===")
        version = input("Enter version name: ").strip()
        source_path = input("Enter source documents path: ").strip()

        if not version or not source_path:
            print("Version name and source path are required.")
            input("Press Enter to continue...")
            return

        try:
            # Initialize version and create vector store
            self.rag_app.conv_manager.init_version(version, source_path)
            self.rag_app.vector_manager.init_vector_store(version, source_path)

            print(f"\nVersion '{version}' initialized successfully!")
            self.current_version = version
            input("Press Enter to continue...")

        except Exception as e:
            print(f"\nError initializing version: {str(e)}")
            input("Press Enter to continue...")

    def _handle_new_conversation(self):
        """Handle starting a new conversation"""
        version = self._select_version("Select version for new conversation")
        if not version:
            return

        try:
            conv_id, _ = self.rag_app.conv_manager.start_conversation(version)
            self.current_version = version
            self.current_conv_id = conv_id

            print(f"\nNew conversation started with ID: {conv_id}")
            self._chat_loop()

        except Exception as e:
            print(f"\nError starting conversation: {str(e)}")
            input("Press Enter to continue...")

    def _handle_update_vector_store(self):
        """Handle updating vector store"""
        version = self._select_version("Select version to update")
        if not version:
            return

        try:
            version_meta = self.rag_app.conv_manager.get_version_meta(version)
            if not version_meta:
                print("Version metadata not found.")
                input("Press Enter to continue...")
                return

            source_path = version_meta["source_path"]
            if self.rag_app.vector_manager.update_vector_store(version, source_path):
                print("\nVector store updated successfully!")
            else:
                print("\nNo changes detected in source files.")

            input("Press Enter to continue...")

        except Exception as e:
            print(f"\nError updating vector store: {str(e)}")
            input("Press Enter to continue...")

    def _handle_list_conversations(self):
        """Handle listing conversations"""
        version = self._select_version("Select version to view conversations")
        if not version:
            return

        conversations = self.rag_app.conv_manager.list_conversations(version)

        print(f"\n=== Conversations for version '{version}' ===")
        if not conversations:
            print("No conversations found.")
        else:
            for i, conv in enumerate(conversations, 1):
                print(f"{i}. {conv['description']} ({conv['id'][:8]}...) - {conv['created_at']}")

        input("\nPress Enter to continue...")

    def _handle_continue_conversation(self):
        """Handle continuing an existing conversation"""
        version = self._select_version("Select version")
        if not version:
            return

        conv_id = self._select_conversation(version)
        if not conv_id:
            return

        self.current_version = version
        self.current_conv_id = conv_id
        self._chat_loop()

    def _handle_exit(self):
        """Handle application exit"""
        print("\nThank you for using Personal RAG System. Goodbye!")
        self.is_running = False

    def _chat_loop(self):
        """Handle the chat interaction loop"""
        if not self.current_conv_id or not self.current_version:
            return

        print("\n=== Chat Mode ===")
        print("Type 'exit' to end the conversation")
        print("Type 'clear' to clear conversation history")
        print("Type 'history' to view conversation history")
        print("=" * 20)

        while True:
            try:
                user_input = input("\nYou: ").strip()

                if user_input.lower() == 'exit':
                    print("Ending conversation...")
                    break
                elif user_input.lower() == 'clear':
                    # Clear conversation history
                    self.rag_app.conv_manager.clear_conversation(
                        self.current_version,
                        self.current_conv_id
                    )
                    print("Conversation history cleared")
                elif user_input.lower() == 'history':
                    # Show conversation history
                    messages = self.rag_app.conv_manager.get_conversation_messages(
                        self.current_version,
                        self.current_conv_id
                    )
                    print("\n=== Conversation History ===")
                    for msg in messages:
                        print(f"{msg['role'].capitalize()}: {msg['content']}")
                    print("=" * 30)
                else:
                    # Process user query
                    response = self.rag_app.query(
                        self.current_version,
                        self.current_conv_id,
                        user_input
                    )
                    print(f"\nAssistant: {response}")

            except KeyboardInterrupt:
                print("\nOperation cancelled by user.")
                break
            except Exception as e:
                print(f"\nAn error occurred: {str(e)}")
                break

        # Reset conversation state
        self.current_conv_id = None
        input("\nPress Enter to return to main menu...")
