 # Personal RAG (Retrieval-Augmented Generation) System

A sophisticated chatbot system that can process, index, and retrieve information from various document sources to provide accurate and context-aware responses to user queries.

## 🚀 Features

- **Document Processing**: Automatically processes various document formats
- **Vector Storage**: Efficient storage and retrieval of document embeddings
- **Conversational AI**: Natural language understanding and response generation
- **Modular Architecture**: Clean separation of concerns between data processing and LLM interactions
- **Customizable**: Easily configurable for different document sources and LLM backends

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/PersonalRAG.git
   cd PersonalRAG
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the project root with:
   ```
   OPENAI_API_KEY=your_openai_api_key
   HF_TOKEN=your_huggingface_token
   ```

## Quick Start

1. Run the application:
   ```bash
   python -m Main
   ```

2. Follow the interactive menu to:
   - Initialize a new document version
   - Start querying your documents
   - Manage conversations
   - Update your document collection

## Usage Guide

### 1. Initialize a New Version

1. Select "Initialize new version" from the main menu
2. Enter a version name (e.g., "research_papers")
3. Provide the path to your document directory

### 2. Start a New Conversation

1. Select "Start new conversation"
2. Choose a version to query
3. Begin asking questions about your documents

### 3. Update Documents

1. Select "Update vector store"
2. Choose the version to update
3. The system will process any changed files

### 4. Continue Previous Conversations

1. Select "Continue conversation"
2. Choose a version and conversation
3. Pick up where you left off

## Project Structure

```
PersonalRAG/
├── Main/                      # Main application package
│   ├── __init__.py
│   ├── __main__.py           # Application entry point
│   ├── app.py                # Core application logic
│   ├── menu.py               # Interactive menu system
│   ├── conversation_manager.py  # Conversation management
│   └── vector_store_manager.py  # Vector store operations
├── DataLayer/                # Data processing modules
│   ├── data_module.py        # File operations
│   └── data_process.py       # Document processing
├── LLMUtils/                 # LLM and RAG utilities
│   ├── RAG.py                # RAG pipeline
│   └── vector_store.py       # Vector store operations
├── config.py                 # Configuration settings
└── requirements.txt          # Python dependencies
```

## Configuration

Edit `config.py` to customize:
- Default model parameters
- File paths
- Chunking and embedding settings

## Troubleshooting

### Querying the System
Interact with the system through the command line:
```
> What information do you have about [topic]?
[System will retrieve and generate a response based on the indexed documents]
```

## ⚙️ Configuration

1. Copy `.env.example` to `.env`
2. Update the `.env` file with your configuration:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `HF_TOKEN`: Your Hugging Face authentication token
   - Other model and processing parameters

### Command Line Arguments
- `--source_path` (required): Path to the directory containing your documents
- `--version` (optional, default="1.0"): Version identifier for the vector store (useful for maintaining different document collections)

## 📚 Dependencies

- Python 3.8+
- LangChain
- Chroma (for vector storage)
- Other dependencies listed in `requirements.txt`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
