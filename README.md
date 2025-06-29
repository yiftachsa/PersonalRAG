# Personal RAG (Retrieval-Augmented Generation) System

A sophisticated chatbot system that can process, index, and retrieve information from various document sources to
provide accurate and context-aware responses to user queries. Built with Python and leveraging state-of-the-art language
models.

## 🚀 Features

- **Document Processing**: Automatically processes various document formats
- **Vector Storage**: Efficient storage and retrieval of document embeddings
- **Conversational AI**: Natural language understanding and response generation
- **Modular Architecture**: Clean separation of concerns between data processing and LLM interactions
- **Version Control**: Manage different versions of your document collections
- **Interactive CLI**: User-friendly command-line interface for easy interaction

## 🛠️ Installation

1. **Prerequisites**:
    - Python 3.8+
    - pip (Python package manager)

2. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/PersonalRAG.git
   cd PersonalRAG
   ```

3. Set up a virtual environment (recommended):
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate
   
   # Unix/MacOS
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up environment variables:
   Copy the example environment file and update it with your credentials:
   ```bash
   copy .env.example .env
   ```
   Then edit the `.env` file with your API keys and configurations.

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
│   ├── app.py                # Core application logic
│   ├── menu.py               # Interactive menu system
├── DataLayer/                # Data processing modules
│   ├── data_module.py        # File operations
│   ├── docling_utils.py      # Docling utilities
│   └── data_process.py       # Document processing
├── LLMUtils/                 # LLM and RAG utilities
│   ├── rag.py                # RAG pipeline
│   ├── compression.py        # LLM compression
│   └── vector_store_utils.py # Vector store operations
├── core/                     # Core functionality
│   ├── __init__.py
│   ├── version.py            # Version management
│   ├── conversation.py       # Conversation handling
│   ├── manager.py            # Manage the flow
│   └── vector_store.py       # Vector store implementations
├── config.py                 # Configuration settings
├── requirements.txt          # Python dependencies
└── .env.example              # Example environment variables
```

## Core Components

1. **Version Management** (`core/version.py`)
    - Handles document versioning and tracking
    - Manages different document collections

2. **Conversation System** (`core/conversation.py`)
    - Manages chat history and context
    - Handles conversation state and persistence

3. **Vector Store** (`core/vector_store.py`)
    - Implements FAISS-based vector storage
    - Handles document embeddings and similarity search

4. **Data Layer** (`DataLayer/`)
    - Processes and prepares documents
    - Handles file operations and data loading

5. **LLM Utilities** (`LLMUtils/`)
    - Implements RAG pipeline
    - Manages language model interactions

## Configuration

### Edit `config.py` to customize:

- Default model parameters
- File paths and storage locations
- Chunking and embedding settings
- Conversation history settings

### Edit `.env`

1. Copy `.env.example` to `.env`
2. Update the `.env` file with your configuration:
    - `OPENAI_API_KEY`: Your OpenAI API key
    - `HF_TOKEN`: Your Hugging Face authentication token
    - Other model and processing parameters

## Common Issues

1. **Missing Dependencies**
   ```bash
   # If you encounter missing packages:
   pip install -r requirements.txt
   ```

2. **Environment Variables**
    - Ensure `.env` file exists and contains all required variables
    - Check for typos in variable names

3. **Memory Issues**
    - Large documents may require more memory
    - Try reducing chunk size in `config.py`

4. **API Rate Limits**
    - Check your API key usage and limits
    - Consider implementing rate limiting if needed

### Command Line Arguments

- `--source_path` (required): Path to the directory containing your documents
- `--version` (optional, default="1.0"): Version identifier for the vector store (useful for maintaining different
  document collections)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
