"""
Embedding Configuration

Centralized configuration for codebase embedding settings.
"""

import os
from typing import Dict, Any

class EmbeddingConfig:
    """Configuration class for embedding settings."""
    
    # OpenAI API Configuration
    OPENAI_API_KEY = "sk-WRDSNGPePp-cHG5Q6WhRjA"
    OPENAI_API_BASE = "https://ciq-litellm-proxy-service.prod-dbx.commerceiq.ai"
    EMBEDDING_MODEL = "openai/text-embedding-3-small"
    LLM_MODEL = "openai/gpt-4o"
    
    # Text Processing Configuration
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 100
    SUPPORTED_EXTENSIONS = ('.java', '.md', '.txt')
    
    # Vectorstore Configuration
    VECTORSTORE_DIR = "codebase_intelligence/vectorstores"
    
    # Codebase Paths
    CODEBASES = {
        "ccp-vap": "/Users/pratyushsingh/Public/github/ccp-vap",
        "ccp-execute": "/Users/pratyushsingh/Public/github/ccp-execute"
    }
    
    @classmethod
    def get_openai_config(cls) -> Dict[str, Any]:
        """Get OpenAI configuration dictionary."""
        return {
            "openai_api_key": cls.OPENAI_API_KEY,
            "openai_api_base": cls.OPENAI_API_BASE,
            "model": cls.EMBEDDING_MODEL
        }
    
    @classmethod
    def get_llm_config(cls) -> Dict[str, Any]:
        """Get LLM configuration dictionary."""
        return {
            "base_url": cls.OPENAI_API_BASE,
            "api_key": cls.OPENAI_API_KEY,
            "model": cls.LLM_MODEL
        } 