from DataLayer.data_module import list_files, get_changed_files, get_prev_files_details, init_date_dir, \
    get_prev_date_dir
from DataLayer.data_process import load_docs_chunks
from Main import Utils
from OOP.vector_store import VectorStore
from OOP.conversation import Conversation


class Version:
    def __init__(self, version_num, data_dir):
        self.version_num = version_num
        self.ver_path = rf"{data_dir}\v_{version_num}"

        # self.source_path = rf"{self.ver_path}\files_details"
        # self.vector_store_path = rf"{self.ver_path}\vector_store"
        self.vectorstore = None
        self.date_path = None
        self.conv = None
        self.convs_path = None

    def init_vector_store(self, source_path):
        self.date_path = init_date_dir(self.ver_path)
        self.vectorstore = VectorStore(self.date_path)
        self.vectorstore.create_vector_store_from_path(source_path)
        self.convs_path = Utils.init_convs(self.date_path)

    def load_vector_store(self):
        self.date_path = get_prev_date_dir(self.ver_path)
        self.vectorstore = VectorStore(self.date_path)
        self.vectorstore.load_vector_store()
        self.convs_path = Utils.get_convs_path(self.date_path)

    def start_conversation(self):
        self.conv = Conversation(convs_dir=self.convs_path)
        conv_retrieval_chain = self.conv.start_conversation(self.vectorstore.get_retriever())
        # return conv_retrieval_chain
        return self.conv.conv_id

    def continue_conversation(self, conv_id):
        self.conv = Conversation(convs_dir=self.convs_path, conv_id=conv_id)
        conv_retrieval_chain = self.conv.continue_conversation(self.vectorstore.get_retriever())
        return self.conv.conv_id

    def query(self, question):
        if not self.conv:
            raise ValueError("No conversation is active. Start or continue a conversation first.")
        return self.conv.query(question)

    def get_messages(self, conv_id=None):
        if not self.conv and not conv_id:
            raise ValueError("No conversation is active. Start or continue a conversation first.")
        if conv_id:
            self.continue_conversation(conv_id)
        return self.conv.get_messages()

    def update_vector_store(self):
        if not self.vectorstore:
            raise ValueError("No vector store is initialized. Initialize a vector store first.")
        # self.date_path = get_prev_date_dir(self.ver_path)
        prev_vector_store = self.vectorstore
        self.vectorstore = None
        self.date_path = None
        self.conv = None
        self.convs_path = None

        # prev_files_details = prev_vector_store.get_files_details()

        self.date_path = init_date_dir(self.ver_path)
        self.vectorstore = VectorStore(self.date_path)
        self.vectorstore.create_vector_store_from_other(prev_vector_store)
        self.convs_path = Utils.init_convs(self.date_path)
