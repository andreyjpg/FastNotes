from ollama import generate

def generate_content_via_llm(propmt: str):
    response = generate(
        model="llama3.2",
        prompt=propmt
        
    )
    return response