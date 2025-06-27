import os

from config import settings
from DataLayer.data_module import init_date_dir, save_dict, load_dict
from version import Version


class Manager:
    def __init__(self):
        self.current_version = None
        # self.current_conv = None
        # self.current_conv_id = None
        # self.retriever = None
        self.data_dir = settings.DATA_DIR

    def init_version(self, version_num: str, source_path: str) -> str:
        """Initialize a new version with source documents"""
        self.current_version = Version(version_num, self.data_dir)
        self.current_version.init_vector_store(source_path)

        return self.current_version.date_path

    def _ensure_version_selected(self, version_num=None):
        if version_num is None and self.current_version is None:
            raise ValueError("No version selected")
        use_current_version_no_arg = version_num is None and self.current_version is not None
        use_current_version_arg = self.current_version and self.current_version.version_num == version_num
        if not (use_current_version_no_arg or use_current_version_arg):
            # try to load different conversation #version_num != self.current_version.version_num:
            self.current_version = Version(version_num, self.data_dir)
            self.current_version.load_vector_store()  # loads latest vector store

    def start_conversation(self, version_num: str = None):
        self._ensure_version_selected(version_num)

        # Start a new conversation in current_version
        conv_id = self.current_version.start_conversation()

        return conv_id

    def continue_conversation(self, version_num, conv_id):
        self._ensure_version_selected(version_num)

        # Continue a conversation in current_version
        conv_id = self.current_version.continue_conversation(conv_id)

        return conv_id

    def query(self, question: str):
        if not self.current_version:
            raise ValueError("No version selected")

        return self.current_version.query(question)

    def get_messages(self, version_num=None, conv_id=None):
        self._ensure_version_selected(version_num)
        if conv_id is None:
            return self.current_version.get_messages()
        else:
            return self.current_version.get_messages(conv_id)

    def _list_data(self, include_convs=False):
        data = []
        for version_name in os.listdir(self.data_dir):
            if not version_name.startswith("v_"):
                continue
            version_path = fr"{self.data_dir}\{version_name}"
            for date in os.listdir(version_path):
                date_path = fr"{version_path}\{date}"
                vector_store_meta = load_dict(fr"{date_path}\vector_store_meta.json")
                source_path = vector_store_meta["source_path"]

                data_dict = {"version": version_name[2:], "source_path": source_path}
                if include_convs:
                    convs_paths = os.listdir(fr"{date_path}\convs")
                    for conv_path in convs_paths:
                        conv_meta = load_dict(fr"{convs_paths}\{conv_path}\conv_meta.json")
                        data_dict["conv_id"] = conv_meta["id"]
                        data_dict["description"] = conv_meta["description"]
                        data.append(data_dict)
        return data

    def list_conversations(self):
        return self._list_data(include_convs=True)

    def list_versions(self):
        return self._list_data(include_convs=False)

    def update_vector_store(self, version_num: str = None):
        self._ensure_version_selected(version_num)

        self.current_version.update_vector_store()
