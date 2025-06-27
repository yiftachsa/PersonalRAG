from langchain.chains.summarize import load_summarize_chain
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import ChatMessageHistory
from langchain.docstore.document import Document
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.schema import messages_to_dict, messages_from_dict
import json

from config import settings


def get_llm(model_name=settings.LLM_MODEL, temp=settings.LLM_TEMP):
    """
    Initialize OpenAI Chat LLM model

    :param model_name: model name
    :param temp: temperature
    :return: llm
    """
    llm = ChatOpenAI(model_name=model_name, temperature=temp)
    return llm


def summarize(text):
    llm = get_llm()
    sum_chain = load_summarize_chain(llm, chain_type="stuff", max_tokens=50)
    docs = [Document(page_content=text)]
    summary = sum_chain.run(docs)

    return summary


def conversation_chain(retriever, llm=None, memory_load_path=None):
    """
    Create a conversational retrieval chain using the given LLM and retriever.
    Conversational Retrieval Chain uses memory to keep track of the conversation history.

    :param llm: LLM. Defaults to get_llm()
    :param retriever: retriever to use
    :return: conversational retrieval chain
    """
    if llm is None:
        llm = get_llm()
    if memory_load_path is not None:
        messages = load_messages_from_file(memory_load_path)
        chat_history = ChatMessageHistory(messages=messages)

        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            chat_memory=chat_history
        )
    else:
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

    conv_retrieval_chain = ConversationalRetrievalChain.from_llm(
        llm,
        retriever=retriever,
        memory=memory,
        # return_source_documents=True,
        # return_generated_question=True,
    )
    return conv_retrieval_chain


def save_memory_to_file(conv_retrieval_chain, save_path):
    memory = conv_retrieval_chain.memory
    messages = memory.chat_memory.messages
    serializable = messages_to_dict(messages)
    with open(fr"{save_path}\"memory.json", "w") as f:
        json.dump(serializable, f)


def load_messages_from_file(load_path):
    with open(fr"{load_path}\"memory.json", "r") as f:
        serializable = json.load(f)
    messages = messages_from_dict(serializable)
    return messages


def retrieval_qa(retriever, chain_type=settings.CHAIN_TYPE, llm=None):
    if llm is None:
        llm = get_llm()
    retrieval_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type=chain_type,  # Chain types: "stuff", "refine", "map_reduce", "map_rerank"
        retriever=retriever,
        # return_source_documents=True,
        verbose=True
    )
    return retrieval_chain


def prompted_retrieval_qa(retriever, chain_type=settings.CHAIN_TYPE, llm=None):
    if llm is None:
        llm = get_llm()

    template = \
        """Use the following pieces of context to answer the question at the end. 
        If you don't know the answer, just say that you don't know, don't try to make up an answer. 
        Use three sentences maximum. Keep the answer as concise as possible. 
        Always say "thanks for asking!" at the end of the answer.
        {context}
        Question: {question}
        Helpful Answer:"""
    prompt_template = PromptTemplate(input_variables=["context", "question"], template=template)
    retrieval_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type=chain_type,  # Chain types: "stuff", "refine", "map_reduce", "map_rerank"
        retriever=retriever,
        # return_source_documents=True,
        chain_type_kwargs={"prompt": prompt_template},
        verbose=True,
    )

    return retrieval_chain
