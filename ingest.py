import os
import re

def clean_text(text):
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text) # Remove markdown links
    text = re.sub(r'http\S+|www\.\S+', '', text) # Remove URLs
    text = re.sub(r'\s+', ' ', text) # Normalize whitespace
    return text.strip()

def chunk_text(text, doc_name, chunk_size=400, overlap=80):
    chunks = []
    start = 0
    text_len = len(text)
    
    while start < text_len:
        end = start + chunk_size
        chunk_data = text[start:end]
        
        if chunk_data.strip():
            chunks.append({
                "text": chunk_data,
                "metadata": {"source": doc_name}
            })
            
        start += (chunk_size - overlap)
        
    return chunks

def get_all_chunks(docs_dir="documents"):
    all_chunks = []
    if not os.path.exists(docs_dir):
        print(f"Error: Directory '{docs_dir}' not found.")
        return []

    for file_name in [f for f in os.listdir(docs_dir) if f.endswith('.txt')]:
        with open(os.path.join(docs_dir, file_name), "r", encoding="utf-8") as f:
            cleaned_content = clean_text(f.read())
            doc_chunks = chunk_text(cleaned_content, doc_name=file_name)
            all_chunks.extend(doc_chunks)
            
    print(f"Pipeline Complete! Generated {len(all_chunks)} total chunks.")
    return all_chunks

if __name__ == "__main__":
    chunks = get_all_chunks()
    print("\n--- Inspecting First 3 Chunks ---")
    for i, c in enumerate(chunks[:3]):
        print(f"\n[Chunk {i+1}] Source: {c['metadata']['source']}\nContent: {c['text']}")