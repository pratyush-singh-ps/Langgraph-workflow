# Codebase Intelligence with LangGraph

A powerful codebase analysis system that uses LangGraph workflows to provide intelligent insights about your code through natural language queries.

## 🚀 Features

- **Semantic Code Search**: Find relevant code using natural language queries
- **Multi-Codebase Support**: Search across multiple codebases simultaneously
- **LangGraph Workflows**: State-based orchestration for complex code analysis
- **Test File Exclusion**: Automatically excludes test files from analysis
- **REST API**: Easy integration via FastAPI endpoints

## 📁 Project Structure

```
Hackathon/
├── codebase_intelligence/     # Core package for code embedding & LangGraph
│   ├── embedding/            # Code file processing and embedding
│   ├── retrieval/            # Semantic search and retrieval
│   ├── orchestration/        # LangGraph workflow management
│   ├── vectorstores/         # Stored FAISS vectorstores
│   ├── config/               # Configuration management
│   └── README.md             # Detailed package documentation
├── main.py                   # FastAPI server
├── requirements.txt          # Dependencies
├── test_new_structure.py     # Test script
└── README.md                 # This file
```

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Hackathon
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up vectorstores** (if not already present)
   ```bash
   python -m codebase_intelligence.embedding.codebase_embedder
   ```

## 🚀 Quick Start

### Start the API Server
```bash
uvicorn main:app --reload
```

### Query the Codebase
```bash
curl -X POST "http://localhost:8000/codebase-query" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "Show me the controller classes",
       "codebase": "both"
     }'
```

### Python Usage
```python
from codebase_intelligence import CodebaseAgent

# Initialize agent
agent = CodebaseAgent()

# Query codebase
response = agent.query_codebase("Show me the controller classes", "both")
print(response)
```

## 📋 API Endpoints

### POST `/codebase-query`
Query the codebase using natural language.

**Request Body:**
```json
{
  "query": "Show me the controller classes",
  "codebase": "both"  // "ccp-vap", "ccp-execute", or "both"
}
```

**Response:**
```json
{
  "response": "Based on the codebase analysis, here are the controller classes..."
}
```

## 🔧 Configuration

All configuration is managed in `codebase_intelligence/config/embedding_config.py`:

- OpenAI API settings
- Model selection
- Chunk sizes for text processing
- Codebase paths

## 🧪 Testing

Run the test script to verify everything is working:
```bash
python test_new_structure.py
```

## 📚 Detailed Documentation

For detailed information about the codebase intelligence package, see:
- [Codebase Intelligence Package Documentation](codebase_intelligence/README.md)

## 🎯 Use Cases

- **Code Discovery**: Find specific implementations or patterns
- **Architecture Analysis**: Understand codebase structure
- **Documentation Generation**: Get explanations of code functionality
- **Onboarding**: Help new developers understand the codebase
- **Code Review**: Identify relevant code for review

## 🔄 Workflow

1. **Embedding**: Code files → Chunks → Embeddings → Vectorstore
2. **Retrieval**: Query → Semantic Search → Relevant Code Chunks
3. **Orchestration**: Context + Query → LLM → Response

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License. 
