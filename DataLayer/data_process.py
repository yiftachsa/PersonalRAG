from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter, TokenTextSplitter
# from langchain.document_loaders import CSVLoader
from langchain_community.document_loaders import CSVLoader
from DataLayer.docling_utils import DOCLING_FILE_TYPES, docling_load


def create_text_splitter(splitter_type: str = None, **kwargs):
    """
    Factory function to create different types of text splitters.

    :param splitter_type: The type of splitter to create ('Character', 'RecursiveCharacter', 'Token').
    :param kwargs: Arguments to pass to the splitter constructor.
    :return: text_splitter: An instance of the specified text splitter.
    """
    if splitter_type is None:
        default_kwargs = {
            "chunk_size": 1000,
            "chunk_overlap": 150,
            "separators": ["\n\n", "\n", "(?<=\. )", " ", ""]
        }
        default_kwargs.update(kwargs)  # allow override of defaults
        return RecursiveCharacterTextSplitter(**default_kwargs)
    elif splitter_type == 'Character':
        return CharacterTextSplitter(**kwargs)
    elif splitter_type == 'RecursiveCharacter':
        return RecursiveCharacterTextSplitter(**kwargs)
    elif splitter_type == 'Token':
        return TokenTextSplitter(**kwargs)
    else:
        raise ValueError(f"Invalid splitter type: {splitter_type}")


def load_csv(csv_file_path):
    """
    Load a CSV file and return a list of documents by row (dicts containing page_content and metadata).
    
    :param csv_file_path: The path to the CSV file. Can contain non-ASCII characters.
    :return: A list of documents (dicts containing page_content and metadata).
    """
    try:
        csv_loader = CSVLoader(
            file_path=csv_file_path,
            encoding='utf-8',
        )
        return csv_loader.load()
    except Exception as e:
        try:
            csv_loader = CSVLoader(
                file_path=csv_file_path,
                encoding='utf-8',
                csv_args={
                    'encoding': 'utf-8',
                    'errors': 'replace'  # Replace invalid characters instead of raising an error
                }
            )
            return csv_loader.load()
        except Exception as e:
            # If UTF-8 fails, try with UTF-8-sig (handles BOM)
            try:
                csv_loader = CSVLoader(
                    file_path=csv_file_path,
                    encoding='utf-8-sig',
                    csv_args={'encoding': 'utf-8-sig'}
                )
                return csv_loader.load()
            except Exception as e:
                # If all else fails, try with the system default encoding
                try:
                    csv_loader = CSVLoader(
                        file_path=csv_file_path,
                        encoding=None,  # Use system default
                        csv_args={'errors': 'replace'}
                    )
                    return csv_loader.load()
                except Exception as final_error:
                    raise RuntimeError(f"Failed to load CSV file {csv_file_path}. Error: {str(final_error)}")


def filter_by_extension(files_paths, extensions=None):
    """
    filter files by extensions, returns a list of file paths.
    :param files_paths: list of file paths.
    :param extensions: list of file extensions.
    :return: list of filtered file paths.
    """
    return [file_path for file_path in files_paths if any(file_path.endswith(ext) for ext in extensions)]


def load_docs_chunks(files_paths, docling_files_types=DOCLING_FILE_TYPES, verbose=False):
    """
    Load chunks from a given list of file paths using both docling and CSV loaders.
    If a file path has an extension in `docling_files_types`, it is loaded using the docling loader.
    .csv files are loaded using CSV loader.

    :param files_paths: list of file paths.
    :param docling_files_types: list of file extensions to load using docling. Default to DOCLING_FILE_TYPES.
    :param verbose: boolean indicating whether to print which files are loaded using which loader.s Defaults to False.
    :return: list of documents chunks.
    """
    filtered_files_docling = filter_by_extension(files_paths, extensions=docling_files_types)
    docling_docs = docling_load(file_paths=filtered_files_docling, text_splitter=create_text_splitter())
    if verbose:
        print("loaded using Docling: ", filtered_files_docling)
    csv_files = filter_by_extension(files_paths, extensions=[".csv"])
    csv_docs = []
    for csv_file in csv_files:
        try:
            csv_docs += load_csv(csv_file)
        except Exception as e:
            print(f"Failed to load CSV file {csv_file}. Error: {str(e)}")
    # csv_docs = [load_csv(csv_file) for csv_file in csv_files] #TODO: Handle errors
    # csv_docs = [doc for sublist in csv_docs for doc in sublist]
    return [*docling_docs, *csv_docs]
