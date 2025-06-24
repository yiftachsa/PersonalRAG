from docling.chunking import HybridChunker
from docling_core.transforms.chunker.tokenizer.openai import OpenAITokenizer
from langchain_docling import DoclingLoader
from langchain_docling.loader import ExportType
import tiktoken

DOCLING_FILE_TYPES = ["pdf", ".docx", ".pptx"]


def process_essential_metadata(dl_meta):
    """
    Process and extract essential metadata from docling metadata.

    :param dl_meta: dict of metadata from docling loader
    :return: dict of processed metadata
    """
    metadata = {}
    metadata['headings'] = ', '.join(dl_meta['headings'])
    # processed_meta['doc_items_count'] = len(dl_meta['doc_items'])  # Count of items
    metadata['doc_items_labels'] = ', '.join([item.get('label', '') for item in dl_meta['doc_items']])
    # metadata['origin_filename'] = dl_meta.get('origin', {}).get('filename', '')
    metadata['type'] = dl_meta.get('origin', {}).get('mimetype', '')

    return metadata


def process_docling_metadata(documents):
    """
    Process and extract docling metadata from docling metadata.
    :param documents:
    :return: dict of processed metadata
    """
    for doc in documents:
        metadata = process_essential_metadata(doc.metadata["dl_meta"])
        # doc.metadata["dl_meta"] = process_essential_metadata(doc.metadata["dl_meta"])
        del doc.metadata["dl_meta"]
        doc.metadata.update(metadata)
    return documents


def docling_load(file_paths, export_type=ExportType.DOC_CHUNKS, model_name="gpt-3.5-turbo",
                 text_splitter=None, process_metadata=True):  # , chunker_strategy=None,):
    """
    Loads chunks from a given file path using docling.
    if no model_name is provided, no chunker will be used.

    :param file_paths: list of Paths to the files to load
    :param export_type: one of DOC_ITEMS, DOC_CHUNKS, DOC_TEXT, DOC_METADATA, DOC_ALL
    :param model_name: The name of the model to use for tokenizing for chunking. If None, no chunking is used.
    :param text_splitter: The text splitter to use for splitting the text after semantic chunking. If None, no splitting is used.
    :param process_metadata: Whether to process the metadata or not. If False, the original metadata is returned
    """
    if model_name is not None:
        tokenizer = OpenAITokenizer(
            tokenizer=tiktoken.encoding_for_model(model_name),
            max_tokens=128 * 1024,  # context window length required for OpenAI tokenizers
        )

        chunker = HybridChunker(
            tokenizer=tokenizer)  # , strategy=chunker_strategy) #https://docling-project.github.io/docling/examples/hybrid_chunking/#configuring-tokenization
    else:
        print("No Chunker will be used")
        chunker = None

    loader = DoclingLoader(  # https://python.langchain.com/docs/integrations/document_loaders/docling/
        file_path=file_paths,
        export_type=export_type,
        chunker=chunker,
    )
    docs = loader.load()

    # Note: Use both chunker and splitter for splitting with overlaps of the semantically chunked paragraphs, which can be long.
    if text_splitter is not None:
        docs = text_splitter.split_documents(docs)

    if process_metadata:
        docs = process_docling_metadata(docs)
    return docs
    # TODO: Markdown

    # if EXPORT_TYPE == ExportType.DOC_CHUNKS:
    #     splits = docs
    # elif EXPORT_TYPE == ExportType.MARKDOWN:
    #     from langchain_text_splitters import MarkdownHeaderTextSplitter

    #     splitter = MarkdownHeaderTextSplitter(
    #         headers_to_split_on=headers_to_split_on,
    #     )
    #     splits = [split for doc in docs for split in splitter.split_text(doc.page_content)]
    # else:
    #     raise ValueError(f"Unexpected export type: {EXPORT_TYPE}")
