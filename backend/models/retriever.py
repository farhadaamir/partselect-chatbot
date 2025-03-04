import os
import openai
from pinecone import Pinecone
from dotenv import load_dotenv

load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX = os.getenv("PINECONE_INDEX")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not PINECONE_API_KEY or not OPENAI_API_KEY:
    raise ValueError("Missing API keys")

# Initializing pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

# accessing pinecone index
index = pc.Index(PINECONE_INDEX)

#no deepseek embedding so just use open ai
def get_openai_embedding(text):
    """generates an embedding vector using OpenAI's API"""

    response = openai.Embedding.create(
        model="text-embedding-3-small",  
        input=text,

        api_key=OPENAI_API_KEY
    )
    return response["data"][0]["embedding"]

def retrieve_relevant_chunks(query, top_k=5):
    """retrieves the most relevant text chunks from Pinecone using OpenAI embeddings"""
    query_embedding = get_openai_embedding(query)

    # Search Pinecone index
    response = index.query(vector=query_embedding, top_k=top_k, include_metadata=True)

    results = []
    for match in response["matches"]:
        metadata = match["metadata"]
        results.append({
            "text": metadata.get("text", ""),
            "brand": metadata.get("brand", "Unknown"),
            "product_type": metadata.get("product_type", "Unknown"),
            "product_page": metadata.get("product_page", "Unknown"),
            "score": match["score"]
        })

    return results

def main():
    """handles user input and retrieves relevant information from Pinecone"""

    while True:
        #terminal testing 
        query = input("Enter your query (or type 'exit' to quit): ").strip()
        if query.lower() == "exit":
            print("Exiting...")
            break

        print(f"\n🔎 Searching for: {query}...")
        results = retrieve_relevant_chunks(query)

        if not results:
            print("No relevant results found.")
        else:
            #print everything once, shorter form for text description
            print("Top results:")
            for i, res in enumerate(results, start=1):
                print(f"Result {i} (Score: {res['score']:.4f})")
                print(f"Brand: {res['brand']}")
                print(f"Product Type: {res['product_type']}")
                print(f"Product Page: {res['product_page']}")
                print(f"Text: {res['text'][:500]}...")  

if __name__ == "__main__":
    main()

