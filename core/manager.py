import os

from dotenv import load_dotenv, find_dotenv
from huggingface_hub import login
from openai import OpenAI

from core.version import Version
from config import settings
from DataLayer.data_module import init_date_dir, save_dict, load_dict


def init_env():
    try:
        _ = load_dotenv(find_dotenv())
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        login(token=settings.HF_TOKEN)
        return client
    except Exception as e:
        print(e)


class Manager:
    """
    Manage multiple versions of the RAG model.

    Each version is associated with a set of source documents, a vector store, and a set of conversations.

    Attributes:
        current_version (Version): The current version being managed.
        data_dir (str): The directory where all versions are stored.
    """

    def __init__(self):
        self.current_version = None
        # self.current_conv = None
        # self.current_conv_id = None
        # self.retriever = None
        self.data_dir = settings.DATA_DIR
        init_env()

    def init_version(self, version_num: str, source_path: str) -> str:
        """Initialize a new version with source documents"""
        self.current_version = Version(version_num, self.data_dir)
        self.current_version.init_vector_store(source_path)

        return self.current_version.date_path

    def _ensure_version_selected(self, version_num=None):
        """
        Ensure a version is selected.

        If version_num is None, it uses the current version if it exists.
        If version_num is not None, it uses the specified version if it exists.
        If no version is selected, it raises an error.
        """
        if version_num is None and self.current_version is None:
            raise ValueError("No version selected")
        use_current_version_no_arg = version_num is None and self.current_version is not None
        use_current_version_arg = self.current_version is not None and self.current_version.version_num == version_num
        if not (use_current_version_no_arg or use_current_version_arg):
            # try to load different conversation #version_num != self.current_version.version_num:
            self.current_version = Version(version_num, self.data_dir)
            self.current_version.load_vector_store()  # loads latest vector store

    def start_conversation(self, version_num: str = None):
        """
        Start a new conversation in the selected version.

        :param version_num: The version of the experiment. If None, use the current version.
        :return: The conversation ID.
        """
        self._ensure_version_selected(version_num)

        # Start a new conversation in current_version
        conv_id = self.current_version.start_conversation()

        return conv_id

    def continue_conversation(self, version_num, conv_id):
        """
        Continue a conversation in the specified version.

        :param version_num: The version of the experiment. If None, use the current version.
        :param conv_id: The conversation ID to continue.
        :return: The conversation ID.
        """
        self._ensure_version_selected(version_num)

        # Continue a conversation in current_version
        conv_id = self.current_version.continue_conversation(conv_id)

        return conv_id

    def query(self, question: str):
        """
        Ask a question in the current conversation.

        :param question: The question to ask.
        :return: The response of the conversation.
        """
        if not self.current_version:
            raise ValueError("No version selected")

        return self.current_version.query(question)

    def get_messages(self, version_num=None, conv_id=None):
        """
        Get the messages of the current conversation.

        If version_num is None, it uses the current version.
        If conv_id is None, it returns the messages of the current conversation.
        If conv_id is not None, it returns the messages of the specified conversation.

        :param version_num: The version of the experiment. If None, use the current version.
        :param conv_id: The conversation ID to get the messages of.
        :return: The messages of the conversation.
        """
        self._ensure_version_selected(version_num)
        if conv_id is None:
            return self.current_version.get_messages()
        else:
            return self.current_version.get_messages(conv_id)

    def _list_data(self, include_convs=False):
        """
        Return a list of dictionaries with information about the versions.

        The list contains dictionaries with the following keys:
            - version (str): The version of the experiment.
            - source_path (str): The path to the source files of the experiment.

        If include_convs is True, the dictionaries also contain a key 'convs' with a list of conversation IDs.

        :param include_convs: If True, include the conversation IDs in the returned dictionaries.
        :return: A list of dictionaries with information about the versions.
        """
        data = []
        for version_name in os.listdir(self.data_dir):
            if not version_name.startswith("v_"):
                continue
            version_path = fr"{self.data_dir}\{version_name}"
            for date in os.listdir(version_path):
                date_path = fr"{version_path}\{date}"
                vector_store_meta = load_dict(fr"{date_path}\vector_store_meta")
                source_path = vector_store_meta["source_path"]

                data_dict = {"version": version_name[2:], "source_path": source_path}
                if include_convs:
                    convs_paths = os.listdir(fr"{date_path}\convs")
                    for conv_path in convs_paths:
                        conv_meta = load_dict(fr"{date_path}\convs\{conv_path}\conv_meta")
                        data_dict["conv_id"] = conv_meta["id"]
                        data_dict["description"] = conv_meta["description"]
                data.append(data_dict)
        return data

    def list_conversations(self):
        """
        Return a list of dictionaries with information about the conversations in the selected version.

        The list contains dictionaries with the following keys:
            - conv_id (str): The conversation ID.
            - description (str): A short description of the conversation.

        :return: A list of dictionaries with information about the conversations.
        """
        return self._list_data(include_convs=True)

    def list_versions(self):
        """
        Return a list of dictionaries with information about the versions.

        The list contains dictionaries with the following keys:
            - version (str): The version of the experiment.
            - source_path (str): The path to the source files of the experiment.

        :return: A list of dictionaries with information about the versions.
        """
        return self._list_data(include_convs=False)

    def update_vector_store(self, version_num: str = None):
        """
        Update the vector store of the specified version.

        If version_num is None, it updates the vector store of the current version.

        :param version_num: The version of the experiment. If None, use the current version.
        """
        self._ensure_version_selected(version_num)

        self.current_version.update_vector_store()
