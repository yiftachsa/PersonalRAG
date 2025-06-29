from DataLayer.data_module import list_files, create_dir, save_dict, load_dict, get_changed_files
from DataLayer.data_process import load_docs_chunks
from LLMUtils.vector_store_utils import create_vector_store, load_vector_store
from LLMUtils.compression import get_compression_retriever

from config import settings


class VectorStore:
    """
    Class to manage vector store.

    Vector store is a set of document vectors that are used to search for relevant documents.
    Vector store is created from a set of documents and it is persisted to disk.
    """
    def __init__(self, date_path):
        self.date_path = date_path

        self.source_path = None
        self.vector_store = None
        self.vector_store_path = None

    def _create_vector_store(self, docs):
        """
        Create a vector store from a list of documents.

        The documents are split into chunks and processed in parallel using joblib.
        The vector store is created from the document chunks and it is persisted to disk.
        The vector store path is saved to a file in the data directory.
        """
        self.vector_store_path = fr"{self.date_path}\vector_store"
        create_dir(self.vector_store_path)
        self.vector_store = create_vector_store(save_path=self.vector_store_path, docs=docs)
        vector_store_meta = {
            "source_path": self.source_path,
        }
        save_dict(vector_store_meta, fr"{self.date_path}\vector_store_meta")

    def create_vector_store_from_path(self, source_path: str) -> str:
        """
        Create a vector store from a given source path.

        The source path is scanned for files and a list of documents is created.
        The documents are processed in parallel using joblib and the vector store is created.
        The vector store path is saved to a file in the data directory.

        :param source_path: The path to the source files.
        :return: The path of the vector store.
        """
        self.source_path = source_path
        # Process documents
        files_details_path = fr"{self.date_path}\files_details"
        source_files_details = list_files(source_path, save_path=files_details_path)
        docs = load_docs_chunks(source_files_details.keys())

        # Create vector store
        self._create_vector_store(docs)
        return self.vector_store_path

    def create_vector_store_from_other(self, other_vector_store):
        """
        Create a vector store from an existing vector store.

        The existing vector store is queried for the source path and the files details.
        The source path is scanned for changed files and a list of documents is created.
        The documents are processed in parallel using joblib and the vector store is created.
        The vector store path is saved to a file in the data directory.

        :param other_vector_store: The vector store to create from.
        :return: The path of the vector store.
        """
        self.source_path = other_vector_store.source_path
        prev_files_details = other_vector_store.get_files_details()

        files_details_path = fr"{self.date_path}\files_details"
        source_files_details = list_files(self.source_path, save_path=files_details_path)

        changed_files = get_changed_files(source_files_details, prev_files_details=prev_files_details)
        if len(changed_files) == 0:
            raise ValueError("No changed files found in source path. No need to update vector store")
        docs = load_docs_chunks(changed_files)

        # Create vector store
        self._create_vector_store(docs)
        return self.vector_store_path

    def get_files_details(self):
        """
        Return the files details of the vector store.

        The files details is a dictionary of file paths and their last modified time.

        :return: The files details of the vector store.
        """
        if self.vector_store is None:
            raise ValueError("Vector store is not initialized. Please create or load a vector store first.")
        files_details_path = fr"{self.date_path}\files_details"
        return load_dict(files_details_path)

    def load_vector_store(self):
        """
        Load the vector store from the date path.

        The vector store path is saved to a file in the data directory.
        The vector store is loaded from the vector store path.

        :return: The path of the vector store.
        """
        self.source_path = load_dict(fr"{self.date_path}\vector_store_meta")["source_path"]

        self.vector_store_path = fr"{self.date_path}\vector_store"
        self.vector_store = load_vector_store(self.vector_store_path)
        return self.vector_store_path

    def get_retriever(self, search_type=settings.SEARCH_TYPE, compress=settings.COMPRESS_QUERY):
        """
        Get a retriever from a vector store based on the settings.

        The vector store path is saved to a file in the data directory.
        The vector store is loaded from the vector store path.
        A retriever is created from the vector store.
        The type of search to perform is determined by the settings.
        If compress is True, the retriever is wrapped in a CompressionRetriever.

        :param search_type: type of search to perform (default: settings.SEARCH_TYPE)
        :param compress: whether to compress retrieved documents (default: settings.COMPRESS_QUERY)
        :return: retriever
        """
        if self.vector_store is None:
            raise ValueError("Vector store is not initialized. Please create or loada vector store first.")
        retriever = self.vector_store.as_retriever(search_type=search_type)  # NOTE: OR SelfQueryRetriever

        if compress:
            retriever = get_compression_retriever(retriever)
        return retriever
