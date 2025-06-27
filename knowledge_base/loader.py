import os

class KnowledgeBaseLoader:
    def __init__(self):
        self.documents = []

    def load_from_directory(self, directory: str):
        self.documents = []
        for filename in os.listdir(directory):
            if filename.endswith('.txt') or filename.endswith('.md'):
                with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f:
                    self.documents.append(f.read())

    def get_documents(self):
        return self.documents 