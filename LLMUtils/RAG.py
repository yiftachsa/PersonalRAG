from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.prompts import PromptTemplate


def get_llm(model_name="gpt-3.5-turbo", temp=0):
    """
    Initialize OpenAI Chat LLM model

    :param model_name: model name
    :param temp: temperature
    :return: llm
    """
    llm = ChatOpenAI(model_name=model_name, temperature=temp)
    return llm


def conversation_chain(retriever, llm=None):
    """
    Create a conversational retrieval chain using the given LLM and retriever.
    Conversational Retrieval Chain uses memory to keep track of the conversation history.

    :param llm: LLM. Defaults to get_llm()
    :param retriever: retriever to use
    :return: conversational retrieval chain
    """
    if llm is None:
        llm = get_llm()
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


def retrieval_qa(retriever, chain_type="stuff", llm=None):
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


def prompted_retrieval_qa(retriever, chain_type="stuff", llm=None):
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
