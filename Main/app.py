import os
from typing import Dict, List, Optional

from menu import MenuSystem
from OOP.manager import Manager


class PersonalRAGApp:
    def __init__(self):
        self.manager = Manager()
        self.menu = MenuSystem()

    def run(self):
        """Main application loop"""
        while True:
            choice = self.menu.show_menu()

            if choice == 1:  # Initialize new version
                self._handle_init_version()
            elif choice == 2:  # Start new conversation
                self._handle_new_conversation()
            elif choice == 3:  # Update vector store
                self._handle_update_vector_store()
            elif choice == 4:  # List conversations
                self._handle_list_conversations()
            elif choice == 5:  # Continue conversation
                self._handle_continue_conversation()
            elif choice == 6:  # Exit
                print("Goodbye!")
                break

    def _handle_init_version(self):
        """Handle version initialization"""
        version_name = self.menu.get_input("Enter version name: ")
        if not version_name:
            return

        source_path = self.menu.get_input("Enter source documents path: ")
        if not source_path:
            return

        try:
            self.manager.init_version(version_name, source_path)
            self.menu.show_message(f"Version '{version_name}' initialized successfully")
        except Exception as e:
            self.menu.show_message(f"Error: {str(e)}")

    def _handle_new_conversation(self):
        """Handle starting a new conversation"""
        versions = self.manager.list_versions()
        version_idx = self.menu.get_version_choice(versions, "Select version for new conversation")

        if version_idx < 0:
            return

        version_name = versions[version_idx]["version"]
        try:
            current_conv_id = self.manager.start_conversation(version_name)
            self.menu.show_message(f"Started new conversation with ID: {current_conv_id}")
            self.menu.chat_loop(self.manager.query, self.manager.get_messages)
        except Exception as e:
            self.menu.show_message(f"Error starting conversation: {str(e)}")

    def _handle_update_vector_store(self):
        """Handle updating vector store"""
        versions = self.manager.list_versions()
        version_idx = self.menu.get_version_choice(versions, "Select version to update")

        if version_idx < 0:
            return

        version_name = versions[version_idx]["version"]
        try:
            self.manager.update_vector_store(version_name)
            self.menu.show_message("Vector store updated successfully")
        except Exception as e:
            self.menu.show_message(f"Error updating vector store: {str(e)}")

    def _handle_list_conversations(self):  # TODO: add lisr conversations per version
        """Handle listing conversations"""
        # versions = self.manager.list_versions()
        # version_idx = self.menu.get_version_choice(versions, "Select version to view conversations")
        #
        # if version_idx < 0:
        #     return

        # version_name = versions[version_idx]["version"]
        convs = self.manager.list_conversations()

        if not convs:
            self.menu.show_message("No conversations found")
            return

        self.menu.show_convs(convs)

    def _handle_continue_conversation(self):
        """Handle continuing an existing conversation"""
        # versions = self.manager.list_versions()
        # version_idx = self.menu.get_version_choice(versions, "Select version")
        #
        # if version_idx < 0:
        #     return
        #
        # version_name = versions[version_idx]["version"]
        convs = self.manager.list_conversations()

        if not convs:
            self.menu.show_message("No conversations found")
            return

        conv_idx = self.menu.get_conversation_choice(convs)
        if conv_idx < 0:
            return
        conv_details = convs[conv_idx]
        self.manager.continue_conversation(conv_details["version"], conv_details["conv_id"])
        self.menu.chat_loop(self.manager.query, self.manager.get_messages)


def main():
    app = PersonalRAGApp()
    app.run()


if __name__ == "__main__":
    main()
