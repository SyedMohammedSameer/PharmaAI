# Medicine RAG System

A lightweight Retrieval-Augmented Generation (RAG) system to answer natural language queries about medications using Gemma 3 (4B) from Ollama.

## Features

- RAG-based QA system for medicine information
- Lightweight architecture using Gemma 3 (4B parameter model) via Ollama
- Simple, user-friendly Streamlit interface
- Local processing of medicine data with sentence transformers

## Prerequisites

- Python 3.8+
- [Ollama](https://ollama.com/) installed and running
- Gemma 3 (4B) model pulled in Ollama

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/medicine-rag.git
cd medicine-rag
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Make sure Ollama is running with the Gemma 3 model:
```bash
ollama serve  # In one terminal
ollama run gemma3:4b  # In another terminal
```

4. Run the application:
```bash
streamlit run app.py
```

## Data Format

The application expects medicine data in JSON format in `data/medicines.json`:

```json
[
  {
    "medicine_id": 1,
    "name": "Tylenol",
    "generic_name": "Acetaminophen",
    "manufacturer": "Johnson & Johnson",
    "dosage": "500-1000 mg orally every 4-6 hours as needed (max ~3000 mg per day for adults)",
    "indications": "Mild to moderate pain, fever reduction",
    "contraindications": "Severe hepatic impairment or active liver disease; hypersensitivity to acetaminophen",
    "side_effects": "Generally well tolerated; possible nausea, rash; hepatotoxicity in overdose",
    "mechanism_of_action": "Inhibits prostaglandin synthesis in the central nervous system, leading to analgesic and antipyretic effects (with minimal anti-inflammatory action)",
    "drug_interactions": "Excessive alcohol use increases risk of liver damage; concurrent use with other acetaminophen-containing products can lead to overdose"
  },
  ...
]
```

## Usage

1. Open the application in your web browser (typically at http://localhost:8501)
2. Type your medicine-related questions in the chat interface
3. The system will retrieve relevant medicine information and generate a response

## System Architecture

- **data_prep.py**: Processes medicine data and creates embeddings
- **retriever.py**: Handles retrieval of relevant medicine information based on queries
- **llm_interface.py**: Interfaces with Ollama to generate responses
- **utils.py**: Helper functions for the application
- **app.py**: Main Streamlit application
