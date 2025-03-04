import os
import requests
from retriever import retrieve_relevant_chunks
from dotenv import load_dotenv
import json

load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"

def generate_rag_response(query: str) -> str:
    """Generate response with proper context handling"""
    try:
        #retrieve context
        context_docs = retrieve_relevant_chunks(query)
        if not context_docs:
            return "I couldn't find relevant information. Please try another question."
        
        #context = "\n".join([d["text"] for d in context_docs])
        context = "\n".join([
        f"Brand: {chunk['brand']}\n"
        f"Product Type: {chunk['product_type']}\n"
        f"Product Page: {chunk['product_page']}\n"
        f"Text: {chunk['text'][:500]}..."
        for chunk in context_docs
    ])
        prompt = f"""Answer using ONLY this context:
        {context}

        Question: {query}
        You are the customer support of partselect, an electronic e-commerce platform. Your job is to assist customers and ensure they go satisfied from the website by
        answering questions they have relating to products and services. Make sure the answers are concise and helpful. DO NOT explicitly refer to the provided context, however use
        it to find answers. No need to mention the names of any customers. :"""
        
        # API call
        response = requests.post(
            DEEPSEEK_URL,
            headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}"},
            json={
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.4,
                "stream": True
            },
            stream=True
        )
        #process response in chunks
        for chunk in response.iter_lines():
            if chunk:
                try:
                    chunk_data = json.loads(chunk.decode("utf-8").replace("data: ", ""))  
                    if "choices" in chunk_data and chunk_data["choices"]:
                        delta_content = chunk_data["choices"][0]["delta"].get("content", "")
                        if delta_content:
                            yield delta_content  

                except json.JSONDecodeError:
                    continue  

    except Exception as e:
        yield f"Error generating response: {str(e)}"

       

if __name__ == "__main__":
    print("RAG Chatbot is running! Type 'exit' to quit.\n")

    while True:
        #terminal testing
        query = input("Ask a question: ").strip()
        if query.lower() == "exit":
            print("Goodbye!\n")
            break  

        response_generator = generate_rag_response(query)
        print("AI Response: ", end="", flush=True)
        for chunk in response_generator:  
            print(chunk, end="", flush=True)

        print("\n")  
        #print(f"AI Response: {response}\n")



