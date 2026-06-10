import os
import gradio as gr
from groq import Groq
from retrieval import setup_vector_store, retrieve_context
from dotenv import load_dotenv

# Load API keys from .env
load_dotenv()

# Initialize Groq client and Vector Store
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
collection = setup_vector_store()

def ask_system(question):
    # 1. Retrieve the top 4 most relevant chunks
    hits = retrieve_context(question, collection, k=4)
    
    # 2. Format the chunks into a context block
    context_text = ""
    sources_set = set()
    for hit in hits:
        context_text += f"\nDocument [{hit['source']}]: {hit['text']}\n"
        sources_set.add(hit['source'])
        
    # 3. Build the strict Grounded System Prompt
    system_prompt = (
        "You are an assistant for answering student questions about Cornell campus dining. "
        "You must answer the user's question using ONLY the provided context below. "
        "If the answer cannot be found in the context, explicitly say 'I don't have enough information on that.' "
        "Do NOT use your general knowledge. "
        "Always cite your sources in your response by referencing the Document name (e.g., 'According to source_2.txt...')."
    )
    
    user_prompt = f"Context:\n{context_text}\n\nQuestion: {question}"
    
    # 4. Send to Groq LLM
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.1, # Keeps the model factual and grounded
        )
        answer = chat_completion.choices[0].message.content
    except Exception as e:
        answer = f"Error generating response: {str(e)}"
        
    # 5. Format the unique sources for the UI sidebar
    sources_list = "\n".join(f"• {s}" for s in sources_set)
    return answer, sources_list

# --- Gradio UI Layout ---
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🐻 The Unofficial Cornell Dining Guide")
    gr.Markdown("Ask a question about campus dining, wait times, or food quality. Answers are grounded purely in student reviews.")
    
    with gr.Row():
        inp = gr.Textbox(label="Your Question", placeholder="e.g., What do students think about Toni Morrison dining hall?")
    
    with gr.Row():
        btn = gr.Button("Ask", variant="primary")
        
    with gr.Row():
        with gr.Column(scale=2):
            answer_out = gr.Textbox(label="Answer", lines=8)
        with gr.Column(scale=1):
            sources_out = gr.Textbox(label="Retrieved From", lines=4)
            
    # Wire up the button and the enter key
    btn.click(fn=ask_system, inputs=inp, outputs=[answer_out, sources_out])
    inp.submit(fn=ask_system, inputs=inp, outputs=[answer_out, sources_out])

if __name__ == "__main__":
    demo.launch()