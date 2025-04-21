import numpy as np
import pickle
import os
from sentence_transformers import SentenceTransformer

class Retriever:
    def __init__(self, processed_data_path="./data/processed_medicines.pkl", model_name="all-MiniLM-L6-v2"):
        """Initialize retriever with processed medicine data."""
        self.model = SentenceTransformer(model_name)
        
        # Load processed data if it exists
        if os.path.exists(processed_data_path):
            with open(processed_data_path, 'rb') as f:
                self.documents = pickle.load(f)
        else:
            self.documents = []
    
    def cosine_similarity(self, vec1, vec2):
        """Calculate cosine similarity between two vectors."""
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        return dot_product / (norm1 * norm2)
    
    def retrieve(self, query, top_k=3):
        """Retrieve most relevant medicine documents for a query."""
        if not self.documents:
            return []
        
        # Generate embedding for the query
        query_embedding = self.model.encode(query)
        
        # Calculate similarity with all documents
        similarities = []
        for doc in self.documents:
            sim = self.cosine_similarity(query_embedding, doc["embedding"])
            similarities.append((doc, sim))
        
        # Sort by similarity (descending) and take top_k
        similarities.sort(key=lambda x: x[1], reverse=True)
        top_results = similarities[:top_k]
        
        return [item[0] for item in top_results]
    
    def retrieve_and_format(self, query, top_k=3):
        """Retrieve and format medicine information for RAG context."""
        results = self.retrieve(query, top_k)
        
        if not results:
            return "No medicine information available."
        
        context = "Here is information about relevant medicines:\n\n"
        for i, doc in enumerate(results):
            context += f"--- MEDICINE {i+1} ---\n"
            context += doc["content"] + "\n\n"
        
        return context