"""
Codebase Embedder

Responsible for:
- Loading code files from specified directories
- Splitting code into chunks for embedding
- Converting code chunks to vector embeddings
- Storing embeddings in FAISS vectorstores
- Excluding test files and directories
"""

# Requirements: pip install langchain langgraph openai tiktoken faiss-cpu
try:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain_community.embeddings import OpenAIEmbeddings
    from langchain_community.vectorstores import FAISS
except ImportError as e:
    print("Missing dependencies. Please run: pip install langchain langgraph openai tiktoken faiss-cpu")
    raise e

import os
from typing import List, Dict, Tuple

class CodebaseEmbedder:
    """
    Handles the embedding process for codebases.
    
    Responsibilities:
    - File loading and filtering (excludes test files)
    - Text splitting into chunks
    - Embedding generation using OpenAI
    - Vectorstore creation and management
    """
    
    def __init__(self, 
                 chunk_size: int = 1000, 
                 chunk_overlap: int = 100,
                 supported_extensions: Tuple[str, ...] = ('.java', '.md', '.txt')):
        """
        Initialize the CodebaseEmbedder.
        
        Args:
            chunk_size: Size of text chunks for embedding
            chunk_overlap: Overlap between chunks
            supported_extensions: File extensions to process
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.supported_extensions = supported_extensions
        
        # Initialize embeddings
        self.embeddings = OpenAIEmbeddings(
            openai_api_key="sk-WRDSNGPePp-cHG5Q6WhRjA",
            openai_api_base="https://ciq-litellm-proxy-service.prod-dbx.commerceiq.ai",
            model="openai/text-embedding-3-small"
        )
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size, 
            chunk_overlap=self.chunk_overlap
        )
    
    def _is_test_file_or_directory(self, path: str) -> bool:
        """
        Check if a file or directory should be excluded as a test.
        
        Args:
            path: File or directory path
            
        Returns:
            True if it's a test file/directory, False otherwise
        """
        path_lower = path.lower()
        return 'test' in path_lower
    
    def load_code_files(self, root_dir: str) -> Tuple[List[str], List[Dict[str, str]]]:
        """
        Load code files from directory, excluding test files.
        
        Args:
            root_dir: Root directory to scan
            
        Returns:
            Tuple of (documents, metadata)
        """
        docs, metadatas = [], []
        
        for dirpath, dirnames, filenames in os.walk(root_dir):
            # Skip directories named 'test' or 'tests'
            if any(self._is_test_file_or_directory(part) for part in dirpath.split(os.sep)):
                continue
                
            for fname in filenames:
                # Skip files with 'test' in the filename
                if self._is_test_file_or_directory(fname):
                    continue
                    
                if fname.endswith(self.supported_extensions):
                    fpath = os.path.join(dirpath, fname)
                    try:
                        with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                            docs.append(f.read())
                            metadatas.append({"source": fpath})
                    except Exception as e:
                        print(f"Error reading {fpath}: {e}")
        
        return docs, metadatas
    
    def split_documents(self, docs: List[str], metadatas: List[Dict[str, str]]) -> Tuple[List[str], List[Dict[str, str]]]:
        """
        Split documents into chunks for embedding.
        
        Args:
            docs: List of documents
            metadatas: List of metadata dictionaries
            
        Returns:
            Tuple of (chunks, chunk_metadata)
        """
        chunks, chunk_metas = [], []
        
        for doc, meta in zip(docs, metadatas):
            doc_chunks = self.text_splitter.split_text(doc)
            for chunk in doc_chunks:
                chunks.append(chunk)
                chunk_metas.append(meta)
        
        return chunks, chunk_metas
    
    def embed_codebase(self, name: str, path: str, output_dir: str = "codebase_intelligence/vectorstores") -> str:
        """
        Embed an entire codebase.
        
        Args:
            name: Name of the codebase
            path: Path to the codebase directory
            output_dir: Directory to save vectorstore
            
        Returns:
            Path to the saved vectorstore
        """
        print(f"Processing {name} codebase...")
        
        # Load and split documents
        docs, metadatas = self.load_code_files(path)
        chunks, chunk_metas = self.split_documents(docs, metadatas)
        
        print(f"Embedding {len(chunks)} chunks for {name}...")
        
        # Create vectorstore
        vectorstore = FAISS.from_texts(chunks, self.embeddings, metadatas=chunk_metas)
        
        # Save vectorstore
        vectorstore_path = os.path.join(output_dir, f"{name}_vectorstore")
        vectorstore.save_local(vectorstore_path)
        
        print(f"Saved {name} vectorstore to {vectorstore_path}")
        return vectorstore_path

# Example usage
if __name__ == "__main__":
    # Define codebases to process
    CODEBASES = {
        "ccp-vap": "/Users/pratyushsingh/Public/github/ccp-vap",
        "ccp-execute": "/Users/pratyushsingh/Public/github/ccp-execute"
    }
    
    embedder = CodebaseEmbedder()
    
    for name, path in CODEBASES.items():
        embedder.embed_codebase(name, path) 