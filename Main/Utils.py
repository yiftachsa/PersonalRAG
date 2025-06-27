from DataLayer.data_module import list_files, get_changed_files, get_prev_files_details
from DataLayer.data_process import load_docs_chunks
from LLMUtils.vectorstore import create_vector_store, load_and_update_vector_store, get_retriever, load_vector_store
from DataLayer.data_module import create_dir, save_dict


def init_convs(ver_path: str) -> str:
    convs_path = fr"{ver_path}\convs"
    create_dir(convs_path)

    return convs_path


def get_convs_path(ver_path: str) -> str:
    return fr"{ver_path}\convs"

