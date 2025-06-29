from DataLayer.data_module import init_date_dir, get_prev_date_dir, delete_date_dir, get_convs_path, init_convs

from core.vector_store import VectorStore
from core.conversation import Conversation


class Version:
    """
    Class to manage a version of the experiment.

    A version is a directory with a source path and a vector store.
    The vector store is created from the source path and it is persisted to disk.
    The vector store path is saved to a file in the data directory.
    """

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
        """
        Initialize a vector store from a given source path.

        The source path is scanned for files and a list of documents is created.
        The documents are processed in parallel using joblib and the vector store is created.
        The vector store path is saved to a file in the data directory.

        :param source_path: The path to the source files.
        :return: The path of the vector store.
        """
        self.date_path = init_date_dir(self.ver_path)
        self.vectorstore = VectorStore(self.date_path)
        self.vectorstore.create_vector_store_from_path(source_path)
        self.convs_path = init_convs(self.date_path)

    def load_vector_store(self):
        """
        Load the vector store from the date path.

        The vector store path is saved to a file in the data directory.
        The vector store is loaded from the vector store path.

        :return: The path of the vector store.
        """
        self.date_path = get_prev_date_dir(self.ver_path)
        self.vectorstore = VectorStore(self.date_path)
        self.vectorstore.load_vector_store()
        self.convs_path = get_convs_path(self.date_path)

    def start_conversation(self):
        """
        Start a new conversation using the vector store.

        The conversation is saved in a directory in the data directory.
        The directory name is 'convs'.
        The conversation ID is returned.

        :return: The ID of the conversation.
        """
        self.conv = Conversation(convs_dir=self.convs_path)
        conv_retrieval_chain = self.conv.start_conversation(self.vectorstore.get_retriever())
        # return conv_retrieval_chain
        return self.conv.conv_id

    def continue_conversation(self, conv_id):
        """
        Continue an existing conversation.

        The conversation is loaded from the data directory.
        The conversation ID is used to load the conversation.
        The vector store is used to get a retriever for the conversation.
        The conversation is continued using the retriever.

        :param conv_id: The ID of the conversation to continue.
        :return: The ID of the conversation.
        """
        self.conv = Conversation(convs_dir=self.convs_path, conv_id=conv_id)
        _ = self.conv.continue_conversation(self.vectorstore.get_retriever())
        return self.conv.conv_id

    def query(self, question):
        """
        Query the active conversation with a question.

        If no conversation is active, a ValueError is raised.
        The query is sent to the conversation and the response is returned.

        :param question: The question to ask the conversation.
        :return: The response of the conversation.
        """
        if not self.conv:
            raise ValueError("No conversation is active. Start or continue a conversation first.")
        return self.conv.query(question)

    def get_messages(self, conv_id=None):
        """
        Get the messages of the current conversation.

        If conv_id is None, it returns the messages of the current conversation.
        If conv_id is not None, it returns the messages of the specified conversation.

        :param conv_id: The conversation ID to get the messages of.
        :return: The messages of the conversation.
        """
        if not self.conv and not conv_id:
            raise ValueError("No conversation is active. Start or continue a conversation first.")
        if conv_id:
            self.continue_conversation(conv_id)
        return self.conv.get_messages()

    def update_vector_store(self):
        """
        Update the vector store with new files.

        The vector store is updated with new files by creating a new vector store and copying the old files to it.
        The new vector store is saved in a new directory in the data directory.
        The old vector store is deleted.

        :return: None
        """
        if not self.vectorstore:
            raise ValueError("No vector store is initialized. Initialize a vector store first.")

        prev_vector_store = self.vectorstore
        new_date_path = init_date_dir(self.ver_path)
        new_vectorstore = VectorStore(new_date_path)
        try:
            new_vectorstore.create_vector_store_from_other(prev_vector_store)
            convs_path = init_convs(new_date_path)

            # update self
            self.date_path = new_date_path
            self.vectorstore = new_vectorstore
            self.convs_path = convs_path
            self.conv = None
        except ValueError as e:
            delete_date_dir(new_date_path)
            e = f"{str(e)} Failed to update vector store. Rolling back to previous vector store."
            raise ValueError(e)
