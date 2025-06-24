from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.llms import OpenAI as langchainLLMsOpenAI


# Wrap our vectorstore
def get_compression_retriever(base_retriever):
    """
    Wraps a retriever with a ContextualCompressionRetriever to compress retrieved documents.
    Uses OpenAI's LLMChainExtractor with GPT-3.5-Turbo-instruct as the base compressor.

    :param base_retriever: The base retriever to wrap.
    :return: A ContextualCompressionRetriever that wraps the base retriever.
    """
    llm_instruct = langchainLLMsOpenAI(temperature=0, model="gpt-3.5-turbo-instruct")
    compressor = LLMChainExtractor.from_llm(llm_instruct)

    compression_retriever = ContextualCompressionRetriever(
        base_compressor=compressor,
        base_retriever=base_retriever
    )
    return compression_retriever
