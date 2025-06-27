import datetime
import json
import os
import uuid

from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import messages_to_dict

from DataLayer.data_module import create_dir, save_dict, load_dict
from LLMUtils.RAG import get_llm, conversation_chain, summarize


class Conversation:
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
        self.conv_retrieval_chain = conversation_chain(retriever)

        conv_meta = {
            "id": self.conv_id,
            "created_at": datetime.now().isoformat(),
            "description": "New conversation",
            # "messages": []
        }
        # conv_retrieval_chain.memory.save_to_file(self.conv_dir / "memory.json")
        save_dict(conv_meta, fr"{self.conv_dir}\conv_meta.json")
        # return self.conv_retrieval_chain

    def continue_conversation(self, retriever):
        self.conv_retrieval_chain = conversation_chain(retriever, memory_load_path=fr"{self.conv_dir}\"memory.json")

        # return self.conv_retrieval_chain

    def query(self, question):
        if self.conv_retrieval_chain is None:
            raise ValueError("Conversation not started")
        # TODO: Add moderation for the question
        response = self.conv_retrieval_chain({"question": question})
        # TODO: Add moderation for the response
        messages = self._save_memory_to_file()
        self._update_conversation_description(messages)
        return response["answer"]

    def get_messages(self):
        if self.conv_retrieval_chain is None:
            raise ValueError("Conversation not started")
        messages = self.conv_retrieval_chain.memory.chat_memory.messages
        serializable = messages_to_dict(messages)
        return messages

    def _save_memory_to_file(self):
        memory = self.conv_retrieval_chain.memory
        messages = memory.chat_memory.messages
        serializable = messages_to_dict(messages)
        with open(fr"{self.conv_dir}\"memory.json", "w") as f:
            json.dump(serializable, f)
        return serializable

    def _update_conversation_description(self, messages):
        text_blocks = [msg['data']['content'] for msg in messages]
        full_text = "\n".join(text_blocks)

        description = summarize(full_text)
        load_conv_meta = load_dict(fr"{self.conv_dir}\conv_meta.json")
        load_conv_meta['description'] = description
        save_dict(load_conv_meta, fr"{self.conv_dir}\conv_meta.json")
