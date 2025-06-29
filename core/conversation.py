import json
import os
import uuid

# from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
# from langchain.memory import ConversationBufferMemory
from langchain_core.messages import messages_to_dict

from DataLayer.data_module import create_dir, save_dict, load_dict
from LLMUtils.rag import get_llm, conversation_chain, summarize


class Conversation:
    """
    A class representing a conversation.

    A conversation is a series of messages that are sent by a user and responded to by a chatbot.
    The conversation is stored in a directory with the conversation ID as the name.
    The conversation directory contains a metadata file with information about the conversation,
    and a subdirectory for each date the conversation was active, containing a file with the
    conversation history.

    Attributes:
        conv_id (str): The ID of the conversation.
        conv_dir (str): The path to the directory where the conversation is stored.
        conv_retrieval_chain (ConversationalRetrievalChain): The conversational retrieval chain
            used to respond to the user.
    """
    def __init__(self, convs_dir, conv_id=None):
        if conv_id is not None:
            self.conv_id = conv_id
            self.conv_dir = fr"{convs_dir}\{self.conv_id}"
            assert os.path.exists(self.conv_dir), f"Conversation {self.conv_id} does not exist"
        else:
            self.conv_id = str(uuid.uuid4())
            self.conv_dir = fr"{convs_dir}\{self.conv_id}"
            create_dir(self.conv_dir)

        self.conv_retrieval_chain = None

    def start_conversation(self, retriever):
        """
        Start a new conversation using the given retriever.

        :param retriever: the retriever to use
        :return: the conversational retrieval chain
        """
        self.conv_retrieval_chain = conversation_chain(retriever)

        conv_meta = {
            "id": self.conv_id,
            # "created_at": datetime.now().isoformat(),
            "description": "New conversation",
            # "messages": []
        }
        # conv_retrieval_chain.memory.save_to_file(self.conv_dir / memory.json")
        save_dict(conv_meta, fr"{self.conv_dir}\conv_meta")
        # return self.conv_retrieval_chain

    def continue_conversation(self, retriever):
        """
        Continue an existing conversation using the given retriever.

        :param retriever: the retriever to use
        :return: the conversational retrieval chain
        """
        self.conv_retrieval_chain = conversation_chain(retriever, memory_load_path=self.conv_dir)

        # return self.conv_retrieval_chain

    def query(self, question):
        """
        Query the conversation with a question.

        :param question: the question to ask
        :return: the response of the conversation
        """
        if self.conv_retrieval_chain is None:
            raise ValueError("Conversation not started")
        # TODO: Add moderation for the question
        response = self.conv_retrieval_chain({"question": question})
        # TODO: Add moderation for the response
        messages = self._save_memory_to_file()
        self._update_conversation_description(messages)
        return response["answer"]

    def get_messages(self):
        """
        Get the messages of the conversation.

        :return: the messages of the conversation
        """
        if self.conv_retrieval_chain is None:
            raise ValueError("Conversation not started")
        messages = self.conv_retrieval_chain.memory.chat_memory.messages
        serializable = messages_to_dict(messages)
        return messages

    def _save_memory_to_file(self):
        """
        Save the memory of the conversation to a file.

        :return: the messages saved
        """
        memory = self.conv_retrieval_chain.memory
        messages = memory.chat_memory.messages
        serializable = messages_to_dict(messages)
        with open(fr"{self.conv_dir}\memory.json", "w") as f:
            json.dump(serializable, f)
        return serializable

    def _update_conversation_description(self, messages):
        """
        Update the conversation description with the latest messages.

        :param messages: the messages of the conversation
        :return: None
        """
        text_blocks = [msg['type'] + ": " + msg['data']['content'] for msg in messages]
        full_text = "\n".join(text_blocks)

        description = summarize(full_text)
        load_conv_meta = load_dict(fr"{self.conv_dir}\conv_meta")
        load_conv_meta['description'] = description
        save_dict(load_conv_meta, fr"{self.conv_dir}\conv_meta")
