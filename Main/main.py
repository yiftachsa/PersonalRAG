import os
from dotenv import load_dotenv, find_dotenv

from huggingface_hub import login
from openai import OpenAI

from DataLayer.data_module import init_date_dir, get_prev_date_dir, save_dict, get_prev_files_details, list_files, \
    get_changed_files
from DataLayer.data_process import load_docs_chunks
from LLMUtils.vector_store import create_vector_store, load_and_update_vector_store, get_retriever
from LLMUtils.RAG import conversation_chain


def init_env():
    try:
        _ = load_dotenv(find_dotenv())
        client = OpenAI()
        login(os.getenv('HF_TOKEN'))
        return client
    except Exception as e:
        print(e)


def initialize(version, source_path):
    # if we want to create a new vector store, we will select a different version.
    # maybe add an 'override' flag to delete the version content and re-create it

    # Load previous data - if exists
    prev_data_path = get_prev_date_dir(version)
    prev_files_details = get_prev_files_details(prev_data_path=prev_data_path, new_source_path=source_path)

    # Init
    open_ai_client = init_env()
    curr_date_dir = init_date_dir(version)

    # Process data
    source_files_details = list_files(source_path, save_path=fr"{curr_date_dir}\files_details")
    changed_files = get_changed_files(source_files_details, prev_files_details=prev_files_details)
    docs_chunks = load_docs_chunks(changed_files)  # NOTE: save the chunks?

    # Vector store
    if prev_data_path is not None:
        vector_store = load_and_update_vector_store(path=fr"{prev_data_path}\vector_store", new_docs=docs_chunks)
    else:
        vector_store = create_vector_store(save_path=fr"{curr_date_dir}\vector_store", docs=docs_chunks)

    retriever = get_retriever(vector_store)

    # Init Conversational Retrieval Chain
    conv_retrieval_chain = conversation_chain(retriever)

    return curr_date_dir, conv_retrieval_chain


def query_loop(conv_retrieval_chain):
    """Interactive loop for querying the conversation chain"""
    print("\nEnter your queries (type 'exit' to quit):")
    while True:
        query = input("\nQuestion: ")
        if query.lower() == 'exit':
            break

        try:
            # Pass the query to the conversation chain
            result = conv_retrieval_chain.invoke({"question": query, "chat_history": []})
            print("\nAnswer:", result["answer"])

        except Exception as e:
            print(f"An error occurred: {str(e)}")


def main(*args, **kwargs):
    # TODO: add try catch to delete curr version if process fails in the middle.
    data_path, conv_retrieval_chain = initialize(version=kwargs["version"], source_path=kwargs["source_path"])

    # Save details
    details = {
        "version": kwargs["version"],
        "source_path": kwargs["source_path"],
    }
    save_dict(details, fr"{data_path}\version_details")

    # Start the query loop
    query_loop(conv_retrieval_chain)


if __name__ == "__main__":
    source = r"D:\Documents\Studies\Documents for higher education\עבודה\Projects\Coursera\LangChain\2 - LangChain Chat with Your Data"
    main(version="1.0", source_path=source)
