import streamlit as st
import os
import json
import subprocess
import time
from pathlib import Path
from src.data_prep import DataPrep
from src.retriever import Retriever
from src.llm_interface import OllamaInterface
from src.utils import save_conversation, format_medicine_info, prepare_sample_medicines_json

# Page configuration
st.set_page_config(
    page_title="Medicine Information Assistant",
    page_icon="💊",
    layout="wide"
)

# Initialize session state for conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "system_initialized" not in st.session_state:
    st.session_state.system_initialized = False

def initialize_system():
    """Initialize the RAG system components with progress reporting."""
    # Header during initialization
    st.header("Initializing Medicine RAG System")
    
    progress_bar = st.progress(0)
    status_container = st.empty()
    
    # Step 1: Check data file
    status_container.info("Step 1/4: Checking medicine data file...")
    progress_bar.progress(10)
    
    # Check if data exists, if not create sample data
    data_path = Path("./data/medicines.json")
    prepare_sample_medicines_json()
    
    status_container.info(f"Step 1/4: Found medicine data with {count_medicines(data_path)} entries")
    progress_bar.progress(25)
    time.sleep(0.5)  # Small delay for UI feedback
    
    # Step 2: Process data if needed
    processed_data_path = Path("./data/processed_medicines.pkl")
    if not processed_data_path.exists():
        status_container.warning("Step 2/4: Need to process medicine data (first run)...")
        status_container.info("This could take a few minutes for 117 medicine entries. Please wait...")
        progress_bar.progress(30)
        
        data_prep = DataPrep()
        data_prep.process_and_save(str(data_path))
        
        status_container.success("Step 2/4: Medicine data processed successfully!")
    else:
        status_container.success("Step 2/4: Using previously processed medicine data")
    
    progress_bar.progress(50)
    time.sleep(0.5)  # Small delay for UI feedback
    
    # Step 3: Initialize retriever
    status_container.info("Step 3/4: Initializing medicine retriever...")
    retriever = Retriever()
    num_docs = len(retriever.documents)
    status_container.success(f"Step 3/4: Retriever initialized with {num_docs} medicine documents")
    
    progress_bar.progress(75)
    time.sleep(0.5)  # Small delay for UI feedback
    
    # Step 4: Check Ollama and LLM
    status_container.info("Step 4/4: Connecting to Ollama service...")
    llm = OllamaInterface()
    
    if llm.health_check():
        status_container.success("Step 4/4: Connected to Ollama service successfully")
        model_available = llm.check_model_available()
        if model_available:
            status_container.success("✅ Gemma3:4b model is available")
        else:
            status_container.error("❌ Gemma3:4b model not found in Ollama. Please run: ollama pull gemma3:4b")
    else:
        status_container.error("❌ Could not connect to Ollama service. Please make sure it's running with: ollama serve")
    
    progress_bar.progress(100)
    time.sleep(1)  # Give user time to see completion
    
    st.session_state.system_initialized = True
    return retriever, llm

def count_medicines(data_path):
    """Count the number of medicines in the data file."""
    try:
        with open(data_path, 'r') as f:
            data = json.load(f)
            return len(data)
    except:
        return 0

def main_chat_interface(retriever, llm):
    """Main chat interface after initialization."""
    # Clear the page
    st.empty()
    
    # Header
    st.title("💊 Medicine Information Assistant")
    st.markdown("""
    Ask questions about medications and get accurate information.
    This system uses a RAG approach with Gemma 3 (4B) from Ollama.
    """)
    
    # Sidebar
    with st.sidebar:
        st.header("About")
        st.info(f"This system provides information about medications from a database of {len(retriever.documents)} drugs.")
        
        st.markdown("#### Sample Questions:")
        st.markdown("- What is Tylenol used for?")
        st.markdown("- What are the side effects of Ibuprofen?")
        st.markdown("- Can I take Advil with blood thinners?")
        st.markdown("- How does Acetaminophen work in the body?")
        
        # System status
        st.header("System Status")
        st.success("✅ Medicine data loaded and processed")
        
        # Check Ollama service
        if llm.health_check():
            st.success("✅ Ollama service running")
        else:
            st.error("❌ Ollama service not detected")
            st.error("Please start Ollama with `ollama serve` and run the Gemma 3 model with `ollama run gemma3:4b`")
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if user_input := st.chat_input("Ask a question about medicines..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Generate response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.info("Retrieving relevant medicine information...")
            
            # Retrieve relevant medicine information
            context = retriever.retrieve_and_format(user_input)
            
            message_placeholder.info("Generating response with LLM...")
            # Generate response with LLM
            response = llm.generate_response(user_input, context)
            
            # Display the response
            message_placeholder.empty()
            st.markdown(response)
            
            # Save the conversation
            save_conversation(user_input, context, response)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})

def main():
    if not st.session_state.system_initialized:
        retriever, llm = initialize_system()
        
        # If initialization successful, move to chat interface
        if st.session_state.system_initialized:
            st.rerun()
    else:
        # Load components
        retriever = Retriever()
        llm = OllamaInterface()
        
        # Display chat interface
        main_chat_interface(retriever, llm)

if __name__ == "__main__":
    main()