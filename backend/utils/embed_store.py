import os
import json
import openai
from pinecone import Pinecone, ServerlessSpec
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX = os.getenv("PINECONE_INDEX")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not PINECONE_API_KEY or not OPENAI_API_KEY:
    raise ValueError("🚨 Missing API keys. Check your .env file.")


pc = Pinecone(api_key=PINECONE_API_KEY)


INDEX_DIMENSION = 1536 
existing_indexes = pc.list_indexes().names()

if PINECONE_INDEX not in existing_indexes:
    print(f"Creating new Pinecone index: {PINECONE_INDEX}")
    pc.create_index(
        name=PINECONE_INDEX,
        dimension=INDEX_DIMENSION,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")  
    )


index = pc.Index(PINECONE_INDEX)

def get_openai_embedding(text):
    """Generates an embedding vector using OpenAI's API."""
    response = openai.Embedding.create(
        model="text-embedding-3-small",  
        input=text,
        api_key=OPENAI_API_KEY
    )
    return response["data"][0]["embedding"]  

def load_data(json_path):
    """Loads chunked text data from a JSON file."""
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"File not found: {json_path}")

    with open(json_path, "r", encoding="utf-8") as file:
        content = file.read().strip()
        if not content:
            raise ValueError(f"JSON file {json_path} is empty! Check chunk_data.py output.")

        try:
            data = json.loads(content)
            if not isinstance(data, list):
                raise ValueError("Unexpected format in JSON. Expected a list of chunk dictionaries.")
            return data
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format in {json_path}: {e}")

def embed_and_store(json_path, batch_size=100):
    """Embeds and stores text chunks in Pinecone using OpenAI embeddings, including metadata."""
    data = load_data(json_path)
    
    vectors = []
    total_chunks = 0  

    for i, chunk_data in enumerate(tqdm(data, desc="Embedding text chunks")):
        text = chunk_data.get("text", "").strip()
        if not text:
            print(f"Skipping empty text chunk at index {i}")
            continue  

        try:
            embedding = get_openai_embedding(text)  
        except Exception as e:
            print(f"Error generating embedding for chunk {i}: {e}")
            continue

        metadata = {
            "text": text,
            "brand": chunk_data.get("brand", "Unknown"),
            "product_type": chunk_data.get("product_type", "Unknown"),
            "product_page": chunk_data.get("product_page", "Unknown")
        }

        vectors.append((str(i), embedding, metadata))
        total_chunks += 1

        
        if len(vectors) >= batch_size:
            index.upsert(vectors)
            vectors = []


    if vectors:
        index.upsert(vectors)

    print(f"Successfully stored {total_chunks} chunks in Pinecone!")

if __name__ == "__main__":
    json_path = "chunks_data.json"  
    print(f"Loading chunked data from `{json_path}`...")
    embed_and_store(json_path)


