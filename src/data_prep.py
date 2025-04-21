import json
import os
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle

class DataPrep:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        """Initialize data preparation with a sentence transformer model."""
        self.model = SentenceTransformer(model_name)
        
    def load_data(self, filepath):
        """Load medicine data from JSON file."""
        with open(filepath, 'r') as f:
            medicines = json.load(f)
        return medicines
    
    def create_medicine_documents(self, medicines):
        """Create documents from medicine data for retrieval."""
        documents = []
        for medicine in medicines:
            # Create a comprehensive text document for each medicine
            content = f"""Medicine: {medicine['name']} ({medicine['generic_name']})
Manufacturer: {medicine['manufacturer']}
Dosage: {medicine['dosage']}
Indications: {medicine['indications']}
Contraindications: {medicine['contraindications']}
Side Effects: {medicine['side_effects']}
Mechanism of Action: {medicine['mechanism_of_action']}
Drug Interactions: {medicine['drug_interactions']}"""
            
            documents.append({
                "medicine_id": medicine["medicine_id"],
                "name": medicine["name"],
                "generic_name": medicine["generic_name"],
                "content": content,
                "metadata": medicine
            })
        return documents
    
    def create_embeddings(self, documents):
        """Create embeddings for medicine documents."""
        texts = [doc["content"] for doc in documents]
        embeddings = self.model.encode(texts)
        
        # Add embeddings to documents
        for i, doc in enumerate(documents):
            doc["embedding"] = embeddings[i]
        
        return documents
    
    def process_and_save(self, input_filepath, output_dir="./data"):
        """Process medicine data and save documents with embeddings."""
        medicines = self.load_data(input_filepath)
        documents = self.create_medicine_documents(medicines)
        documents_with_embeddings = self.create_embeddings(documents)
        
        # Save processed data
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, "processed_medicines.pkl"), 'wb') as f:
            pickle.dump(documents_with_embeddings, f)
            
        return documents_with_embeddings

if __name__ == "__main__":
    data_prep = DataPrep()
    data_prep.process_and_save("./data/medicines.json")
    print("Data processing complete. Embeddings created and saved.")