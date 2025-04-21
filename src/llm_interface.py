import json
import subprocess
import requests

class OllamaInterface:
    def __init__(self, model_name="gemma3:4b", base_url="http://localhost:11434"):
        """Initialize Ollama interface."""
        self.model_name = model_name
        self.base_url = base_url
        
    def check_model_available(self):
        """Check if the specified model is available in Ollama."""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            models = response.json().get("models", [])
            return any(model.get("name") == self.model_name for model in models)
        except Exception as e:
            print(f"Error checking model availability: {str(e)}")
            return False
    
    def generate_response(self, prompt, context, max_tokens=1024, temperature=0.7):
        """Generate a response using the LLM with the given prompt and context."""
        # Combine context and prompt
        system_message = "You are a helpful medical information assistant. Provide accurate information based on the medical data provided. If you're unsure or if the information isn't in the provided context, say so."
        full_prompt = f"{system_message}\n\nCONTEXT:\n{context}\n\nQUESTION: {prompt}\n\nANSWER:"
        
        try:
            # Call Ollama API
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": full_prompt,
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens
                    }
                }
            )
            
            if response.status_code == 200:
                return response.json().get("response", "")
            else:
                return f"Error generating response: {response.text}"
        
        except Exception as e:
            return f"Error communicating with Ollama: {str(e)}"
    
    def health_check(self):
        """Check if Ollama service is running by querying /api/tags."""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            return response.status_code == 200
        except:
            return False