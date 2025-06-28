#!/usr/bin/env python3
"""
Test script for the new codebase intelligence structure.
"""

def test_imports():
    """Test that all components can be imported correctly."""
    try:
        print("Testing imports...")
        
        # Test main package import
        from codebase_intelligence import CodebaseEmbedder, CodebaseRetriever, CodebaseAgent
        print("✅ Main package imports successful")
        
        # Test individual module imports
        from codebase_intelligence.embedding import CodebaseEmbedder
        from codebase_intelligence.retrieval import CodebaseRetriever
        from codebase_intelligence.orchestration import CodebaseAgent
        print("✅ Individual module imports successful")
        
        # Test configuration import
        from codebase_intelligence.config.embedding_config import EmbeddingConfig
        print("✅ Configuration import successful")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_configuration():
    """Test configuration functionality."""
    try:
        from codebase_intelligence.config.embedding_config import EmbeddingConfig
        
        # Test config methods
        openai_config = EmbeddingConfig.get_openai_config()
        llm_config = EmbeddingConfig.get_llm_config()
        
        print("✅ Configuration methods work correctly")
        print(f"   OpenAI config keys: {list(openai_config.keys())}")
        print(f"   LLM config keys: {list(llm_config.keys())}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_retriever_initialization():
    """Test retriever initialization."""
    try:
        from codebase_intelligence.retrieval import CodebaseRetriever
        
        retriever = CodebaseRetriever()
        print("✅ Retriever initialization successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Retriever initialization failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing new codebase intelligence structure...\n")
    
    tests = [
        ("Import Test", test_imports),
        ("Configuration Test", test_configuration),
        ("Retriever Test", test_retriever_initialization),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"Running {test_name}...")
        if test_func():
            passed += 1
        print()
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! New structure is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main() 