from DataLayer.data_module import list_files, create_dir, save_dict, load_dict, get_changed_files
from DataLayer.data_process import load_docs_chunks
from LLMUtils.vectorstore import create_vector_store, load_vector_store
from LLMUtils.compression import get_compression_retriever

from config import settings


class VectorStore:
    def __init__(self, date_path):
        self.date_path = date_path

        self.source_path = None
        self.vector_store = None
        self.vector_store_path = None

    def _create_vector_store(self, docs):
        self.vector_store_path = fr"{self.date_path}\vector_store"
        create_dir(self.vector_store_path)
        self.vector_store = create_vector_store(save_path=self.vector_store_path, docs=docs)
        vector_store_meta = {
            "source_path": self.source_path,
        }
        save_dict(vector_store_meta, fr"{self.date_path}\vector_store_meta")

    def create_vector_store_from_path(self, source_path: str) -> str:
        self.source_path = source_path
        # Process documents
        files_details_path = fr"{self.date_path}\files_details"
        source_files_details = list_files(source_path, save_path=files_details_path)
        docs = load_docs_chunks(source_files_details.keys())

        # Create vector store
        self._create_vector_store(docs)
        return self.vector_store_path

    def create_vector_store_from_other(self, other_vector_store):
        self.source_path = other_vector_store.source_path
        prev_files_details = other_vector_store.get_files_details()

        files_details_path = fr"{self.date_path}\files_details"
        source_files_details = list_files(self.source_path, save_path=files_details_path)

        changed_files = get_changed_files(source_files_details, prev_files_details=prev_files_details)
        docs = load_docs_chunks(changed_files)

        # Create vector store
        self._create_vector_store(docs)
        return self.vector_store_path

    def get_files_details(self):
        if self.vector_store is None:
            raise ValueError("Vector store is not initialized. Please create or load a vector store first.")
        files_details_path = fr"{self.date_path}\files_details"
        return load_dict(files_details_path)

    def load_vector_store(self):
        self.source_path = load_dict(fr"{self.date_path}\vector_store_meta")["source_path"]

        self.vector_store_path = fr"{self.date_path}\vector_store"
        self.vector_store = load_vector_store(self.vector_store_path)
        return self.vector_store_path

    def get_retriever(self, search_type=settings.SEARCH_TYPE, compress=settings.COMPRESS_QUERY):
        if self.vector_store is None:
            raise ValueError("Vector store is not initialized. Please create or loada vector store first.")
        retriever = self.vector_store.as_retriever(search_type=search_type)  # NOTE: OR SelfQueryRetriever

        if compress:
            retriever = get_compression_retriever(retriever)
        return retriever
