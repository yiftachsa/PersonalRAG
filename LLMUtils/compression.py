from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
# from langchain.llms import OpenAI as langchainLLMsOpenAI
from langchain_community.llms import OpenAI as langchainLLMsOpenAI

from config import settings


# Wrap our vectorstore
def get_compression_retriever(base_retriever, model=settings.LLM_MODEL_COMPRESS,
                              temperature=settings.LLM_TEMP_COMPRESS):
    """
    Wraps a retriever with a ContextualCompressionRetriever to compress retrieved documents.
    Uses OpenAI's LLMChainExtractor with GPT-3.5-Turbo-instruct as the base compressor.

    :param base_retriever: The base retriever to wrap.
    :param model: The model to use for the base compressor.
    :param temperature: The temperature to use for the base compressor.
    :return: A ContextualCompressionRetriever that wraps the base retriever.
    """
    llm_instruct = langchainLLMsOpenAI(model=model, temperature=temperature)
    compressor = LLMChainExtractor.from_llm(llm_instruct)

    compression_retriever = ContextualCompressionRetriever(
        base_compressor=compressor,
        base_retriever=base_retriever
    )
    return compression_retriever
