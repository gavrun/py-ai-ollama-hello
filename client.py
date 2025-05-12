import requests

# Ollama client adapter

def ask_ollama(prompt, model="phi4"):
    """Generate API request to local Ollama server"""

    url = "http://localhost:11434/api/generate"
    
    payload = {
        "model": model,     # model to use
        "prompt": prompt,   # actual prompt text
        "stream": False     # tokens streaming 
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        return f"[Error] Failed to connect to Ollama: {e}"
    