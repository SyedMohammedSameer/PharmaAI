# Use Python 3.10 as base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies for Ollama
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port for Streamlit
EXPOSE 8501

# Start Ollama service and run the application
CMD bash -c "ollama serve &>/dev/null & \
    sleep 5 && \
    ollama pull gemma3:4b &>/dev/null && \
    echo 'Ollama and Gemma3 model are ready!' && \
    streamlit run app.py"