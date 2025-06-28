# Codebase Intelligence Package

A comprehensive package for embedding, retrieving, and orchestrating codebase analysis using LangGraph workflows.

## 📁 Package Structure

```
codebase_intelligence/
├── embedding/                 # Code embedding and processing
│   ├── __init__.py
│   └── codebase_embedder.py   # Handles code file embedding
├── retrieval/                 # Semantic search and retrieval
│   ├── __init__.py
│   └── codebase_retriever.py  # Manages vectorstore retrieval
├── orchestration/             # LangGraph workflow management
│   ├── __init__.py
│   └── codebase_agent.py      # Main agent orchestrating workflows
├── vectorstores/              # Stored FAISS vectorstores
│   ├── ccp-execute_vectorstore/
│   └── ccp-vap_vectorstore/
├── config/                    # Configuration management
│   └── embedding_config.py    # Centralized configuration
└── README.md                  # This file
```

## 🎯 Component Responsibilities

### 1. **Embedding Module** (`embedding/`)
**Purpose**: Convert code files into vector embeddings for semantic search

**Responsibilities**:
- Load and filter code files (excludes test files)
- Split code into manageable chunks
- Generate embeddings using OpenAI
- Store embeddings in FAISS vectorstores

**Key Features**:
- Automatic test file exclusion
- Configurable chunk sizes and overlap
- Support for multiple file types (Java, Markdown, Text)

### 2. **Retrieval Module** (`retrieval/`)
**Purpose**: Perform semantic search on embedded code

**Responsibilities**:
- Load pre-built FAISS vectorstores
- Execute semantic similarity search
- Retrieve relevant code chunks
- Format results for context

**Key Features**:
- Multi-codebase search support
- Configurable result counts
- Rich metadata preservation

### 3. **Orchestration Module** (`orchestration/`)
**Purpose**: Coordinate the complete codebase analysis workflow

**Responsibilities**:
- Build and manage LangGraph workflows
- Coordinate between retrieval and generation
- Manage conversation state
- Provide unified query interface

**Key Features**:
- State-based workflow management
- LLM integration for response generation
- Error handling and logging

### 4. **Configuration Module** (`config/`)
**Purpose**: Centralized configuration management

**Responsibilities**:
- API key and endpoint configuration
- Model selection and parameters
- File processing settings
- Codebase path management

## 🚀 Usage Examples

### Basic Usage
```python
from codebase_intelligence import CodebaseAgent

# Initialize the agent
agent = CodebaseAgent()

# Query the codebase
response = agent.query_codebase("Show me the controller classes", "both")
print(response)
```

### Embedding New Codebases
```python
from codebase_intelligence.embedding import CodebaseEmbedder

# Initialize embedder
embedder = CodebaseEmbedder()

# Embed a codebase
embedder.embed_codebase("my-codebase", "/path/to/codebase")
```

### Direct Retrieval
```python
from codebase_intelligence.retrieval import CodebaseRetriever

# Initialize retriever
retriever = CodebaseRetriever()

# Search for specific code
docs = retriever.retrieve_from_vap("service implementation", k=5)
```

## 🔧 Configuration

All configuration is centralized in `config/embedding_config.py`:

```python
from codebase_intelligence.config.embedding_config import EmbeddingConfig

# Get OpenAI config
openai_config = EmbeddingConfig.get_openai_config()

# Get LLM config
llm_config = EmbeddingConfig.get_llm_config()
```

## 📋 Dependencies

Required packages:
- `langchain`
- `langgraph`
- `openai`
- `tiktoken`
- `faiss-cpu`

Install with:
```bash
pip install langchain langgraph openai tiktoken faiss-cpu
```

## 🔄 Workflow

1. **Embedding Phase**: Code files → Chunks → Embeddings → Vectorstore
2. **Retrieval Phase**: Query → Semantic Search → Relevant Code Chunks
3. **Orchestration Phase**: Context + Query → LLM → Response

## 🎯 Key Benefits

- **Modular Design**: Each component has clear responsibilities
- **Scalable**: Easy to add new codebases or modify workflows
- **Configurable**: Centralized configuration management
- **Test-Friendly**: Automatic exclusion of test files
- **Production-Ready**: Error handling and logging throughout 