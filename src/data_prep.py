import json
import os
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle
import time

class DataPrep:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        """Initialize data preparation with a sentence transformer model."""
        print(f"Initializing SentenceTransformer with model: {model_name}")
        self.model = SentenceTransformer(model_name)
        print("SentenceTransformer model loaded successfully")
        
    def load_data(self, filepath):
        """Load medicine data from JSON file."""
        print(f"Loading medicine data from: {filepath}")
        start_time = time.time()
        with open(filepath, 'r', encoding='utf-8') as f:  # Specify UTF-8 encoding
            medicines = json.load(f)
        print(f"Loaded {len(medicines)} medicine entries in {time.time() - start_time:.2f} seconds")
        return medicines
    
    def create_medicine_documents(self, medicines):
        """Create documents from medicine data for retrieval."""
        print(f"Creating structured documents for {len(medicines)} medicines")
        start_time = time.time()
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
        print(f"Documents created in {time.time() - start_time:.2f} seconds")
        return documents
    
    def create_embeddings(self, documents):
        """Create embeddings for medicine documents."""
        print(f"Generating embeddings for {len(documents)} documents")
        start_time = time.time()
        
        texts = [doc["content"] for doc in documents]
        print("Encoding texts with SentenceTransformer...")
        embeddings = self.model.encode(texts, show_progress_bar=True)
        
        # Add embeddings to documents
        for i, doc in enumerate(documents):
            doc["embedding"] = embeddings[i]
        
        print(f"Embeddings created in {time.time() - start_time:.2f} seconds")
        return documents
    
    def process_and_save(self, input_filepath, output_dir="./data"):
        """Process medicine data and save documents with embeddings."""
        print(f"Starting data processing pipeline for: {input_filepath}")
        total_start_time = time.time()
        
        medicines = self.load_data(input_filepath)
        documents = self.create_medicine_documents(medicines)
        documents_with_embeddings = self.create_embeddings(documents)
        
        # Save processed data
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "processed_medicines.pkl")
        print(f"Saving processed data to: {output_path}")
        
        with open(output_path, 'wb') as f:
            pickle.dump(documents_with_embeddings, f)
        
        print(f"Data processing complete in {time.time() - total_start_time:.2f} seconds")
        print(f"Total documents processed: {len(documents_with_embeddings)}")
        
        return documents_with_embeddings

if __name__ == "__main__":
    data_prep = DataPrep()
    data_prep.process_and_save("./data/medicines.json")
    print("Data processing complete. Embeddings created and saved.")