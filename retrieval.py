import chromadb
from chromadb.utils import embedding_functions
from ingest import get_all_chunks

def setup_vector_store():
    # Initialize a local, persistent database folder
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    
    # Set up the embedding model to run 100% locally
    default_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    
    # Create or fetch the dining collection
    collection = chroma_client.get_or_create_collection(
        name="cornell_dining_guide", 
        embedding_function=default_ef
    )
    
    chunks = get_all_chunks()
    
    # Add chunks only if database is completely empty to prevent duplicates
    if collection.count() == 0:
        print(f"Loading {len(chunks)} chunks into ChromaDB...")
        
        ids = [f"id_{i}" for i in range(len(chunks))]
        documents = [c["text"] for c in chunks]
        metadatas = [c["metadata"] for c in chunks]
        
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print("Vector database populated successfully!")
    else:
        print(f"Collection already exists with {collection.count()} chunks.")
        
    return collection

def retrieve_context(query, collection, k=4):
    """
    Queries ChromaDB and returns the top-k most relevant text chunks 
    along with their source metadata for attribution.
    """
    results = collection.query(
        query_texts=[query],
        n_results=k
    )
    
    formatted_results = []
    for doc, meta, dist in zip(results['documents'][0], results['metadatas'][0], results['distances'][0]):
        formatted_results.append({
            "text": doc,
            "source": meta["source"],
            "distance": dist
        })
    return formatted_results

if __name__ == "__main__":
    collection = setup_vector_store()
    
    # Run a test query from our Evaluation Plan
    test_query = "What is the general consensus on the quality of Toni Morrison Dining Hall?"
    #test_query = "Is it easy to sneak food out of the dining halls?"
    print(f"\n--- Testing Retrieval for Query: '{test_query}' ---")
    
    hits = retrieve_context(test_query, collection)
    for idx, hit in enumerate(hits):
        print(f"\n[Match {idx+1}] Source: {hit['source']} | Distance Score: {hit['distance']:.4f}")
        print(f"Excerpt: {hit['text']}")