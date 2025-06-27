class KnowledgeBaseRetriever:
    def __init__(self, loader=None):
        self.loader = loader

    def retrieve(self, prompt: str) -> str:
        if self.loader is None or not hasattr(self.loader, 'get_documents'):
            return "[No knowledge base loaded]"
        docs = self.loader.get_documents()
        # Simple keyword search: return the first doc containing a keyword from the prompt
        for doc in docs:
            for word in prompt.split():
                if word.lower() in doc.lower():
                    return doc[:500]  # Return first 500 chars for brevity
        return "[No relevant context found in knowledge base]" 