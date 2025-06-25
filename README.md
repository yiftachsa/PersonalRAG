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

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   # or
   source .venv/bin/activate  # On Unix or MacOS
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Update the environment variables with your API keys and configurations

## 🏃‍♂️ Quick Start

1. Prepare your documents in a directory of your choice
2. Run the main application by specifying the source directory path:
   ```bash
   python -m Main.main --source_path "path/to/your/documents" --version "1.0"
   ```
   Example:
   ```bash
   python -m Main.main --source_path "D:/Documents/MyDocuments" --version "1.0"
   ```
3. Interact with the chatbot through the command-line interface

## 🏗️ Project Structure

```
PersonalRAG/
├── DataLayer/           # Data processing and management
│   ├── data_module.py   # Core data handling
│   └── data_process.py  # Document processing utilities
├── LLMUtils/           # LLM-related functionality
│   ├── RAG.py          # RAG implementation
│   ├── compression.py   # Text compression utilities
│   └── vector_store.py  # Vector storage and retrieval
├── Main/               # Main application entry points
│   └── main.py         # Main application script
├── .env                # Environment variables
└── README.md           # This file
```

## 🤖 Usage

### Loading Documents
Specify the path to your documents directory when running the application. The system will process all supported file formats in the specified directory and its subdirectories.

Supported formats include:
- PDF documents (.pdf)
- Word documents (.docx)
- PowerPoint presentations (.pptx)
- CSV files (.csv)

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
- PyTorch
- Transformers
- LangChain
- FAISS (for vector storage)
- Other dependencies listed in `requirements.txt`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
