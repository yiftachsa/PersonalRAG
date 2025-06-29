import os
# from langchain.embeddings import OpenAIEmbeddings
# from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings

# from langchain.vectorstores import Chroma
from langchain_community.vectorstores import Chroma
from LLMUtils.compression import get_compression_retriever
from config import settings


def get_embedding_model():
    embedding_model = OpenAIEmbeddings(model=settings.EMBEDDING_MODEL)
    return embedding_model


def load_vector_store(path):
    """
    Load vector store from disk
    :param path: path to Chroma vector store
    :return: loaded vector store
    """
    embedding_model = get_embedding_model()

    vector_store = Chroma(persist_directory=path, embedding_function=embedding_model)
    return vector_store


def update_vector_store(vector_store, new_docs):
    """
    Update vector store with new documents

    :param vector_store: vector store to update
    :param new_docs: documents to add
    :return: updated vector store
    """
    vector_store.add_documents(new_docs)
    vector_store.persist()


def load_and_update_vector_store(path, new_docs):
    """
    Load vector store from disk, add new documents and save back to disk.

    :param path: path to Chroma vector store
    :param new_docs: documents to add
    :return: updated vector store
    """
    vector_store = load_vector_store(path)
    if len(new_docs) > 0:
        update_vector_store(vector_store,
                            new_docs)  # TODO: Delete ('forget') old documents versions before update. Can be done using changed_files and iterating with vector_store.delete()
    return vector_store


def create_vector_store(save_path, docs):
    """
    Creates a new vector store from a list of documents.

    :param docs: list of documents to create vector store from
    :param save_path: directory to save vector store to
    :return: vector store
    """
    embedding_model = get_embedding_model()

    vector_store = Chroma.from_documents(
        documents=docs,
        embedding=embedding_model,
        persist_directory=save_path
    )
    # vector_store.persist()
    return vector_store


def get_retriever(vector_store, search_type=settings.SEARCH_TYPE, compress=settings.COMPRESS_QUERY):
    retriever = vector_store.as_retriever(search_type=search_type)  # NOTE: OR SelfQueryRetriever

    if compress:
        retriever = get_compression_retriever(retriever)
    return retriever
