import gradio as gr
from huggingface_hub import InferenceClient
import os

# --- Configuration ---
# Using Qwen 2.5 as requested
MODEL_ID = "Qwen/Qwen2.5-7B-Instruct"
HF_API_TOKEN = "InsertAPIkeyhere"

# --- CSS Styling ---
# Custom CSS to make the UI look like a professional graduation project
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap');

body { font-family: 'Poppins', sans-serif !important; }

.main-container {
    max-width: 900px;
    margin: auto;
}

.header-container {
    text-align: center;
    background: #ffffff; 
    color: #000000;      /* Changed to Black */
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 20px;
    border: 2px solid #e5e7eb; /* Neutral gray border */
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}

.task-title {
    font-size: 2.0rem;
    font-weight: 700;
    margin: 0;
    letter-spacing: 0.5px;
    color: #000000; /* Changed to Black */
}

.sub-title {
    font-size: 1rem;
    font-weight: 400; 
    margin-top: 5px;
    color: #000000; /* Changed to Black */
    opacity: 0.8;
}

.footer-container {
    text-align: center;
    margin-top: 30px;
    padding-top: 15px;
    border-top: 1px solid #e5e7eb;
    color: #4b5563;
    font-size: 0.9rem;
}

.author-name {
    font-weight: 600;
    color: #dc2626; 
}

/* Response Box Styling - UPDATED: White Background & Black Text */
.response-box-success {
    background-color: #6b0606; /* White Background */
    border: 1px solid #22c55e;
    border-left: 5px solid #15803d;
    border-radius: 8px;
    padding: 15px;
    color: #000000; /* Black Text */
}

.response-box-error {
    background-color: #6b0606; /* White Background */
    border: 1px solid #ef4444;
    border-left: 5px solid #b91c1c;
    border-radius: 8px;
    padding: 15px;
    color: #6b0606; /* Black Text */
}

.response-box-uncertain {
    background-color: #6b0606; /* White Background */
    border: 1px solid #f59e0b;
    border-left: 5px solid #b45309;
    border-radius: 8px;
    padding: 15px;
    color: #6b0606; /* Black Text */
}
"""

# --- Evaluation Logic ---
def evaluate_response(prompt, response):
    """Evaluates the model's response quality"""
    if not response:
        return "❌ Error", "No response received"
        
    if response.startswith("Error") or "model_not_supported" in response:
        return "❌ Technical Error", f"Details: {response}"

    if len(response.strip()) == 0:
        return "❌ Not Understood", "Model generated empty response"
    
    # Indicators
    response_lower = response.lower()
    positive_indicators = [
        "sure", "here is", "answer", "steps", "below", "following", "certainly",
        "نعم", "هو", "هي", "الإجابة", "الحل", "تفضل", "بالتأكيد", "طبعاً"
    ]
    
    if any(i in response_lower for i in positive_indicators) or len(response.split()) > 10:
        return "✅ Understood", "Model provided a clear and detailed answer."
    
    return "⚠️ Uncertain", "Response is too short or ambiguous."

# --- Generation Logic ---
def generate_response(prompt_text):
    if not HF_API_TOKEN:
        return "Error: HF_API_TOKEN is missing. Please add it in Settings > Secrets."
    
    client = InferenceClient(token=HF_API_TOKEN)
    
    try:
        messages = [{"role": "user", "content": prompt_text}]
        
        response = client.chat_completion(
            model=MODEL_ID,
            messages=messages,
            max_tokens=600,
            temperature=0.7
        )
        
        return response.choices[0].message.content
            
    except Exception as e:
        return f"Error: {str(e)}"

# --- Main Processing Function ---
def process_prompt(prompt_text):
    if not prompt_text: 
        return "", "⚠️ Warning", "Please enter a prompt."
    
    response_text = generate_response(prompt_text)
    evaluation, reason = evaluate_response(prompt_text, response_text)
    
    # Dynamic HTML styling based on result
    if "Error" in response_text or "Error" in evaluation:
        css_class = "response-box-error"
        header_text = "Error encountered:"
    elif "Understood" in evaluation:
        css_class = "response-box-success"
        header_text = "Model Response:"
    else:
        css_class = "response-box-uncertain"
        header_text = "Model Response (Uncertain):"
    
    html_output = f"""
    <div class="{css_class}">
        <strong style="font-size: 1rem;">{header_text}</strong><br>
        <p style="white-space: pre-wrap; margin-top: 8px; line-height: 1.5; font-size: 0.95rem;">{response_text}</p>
    </div>
    """
    return html_output, evaluation, reason

# --- UI Construction ---
with gr.Blocks(css=custom_css, theme=gr.themes.Soft(primary_hue="blue")) as demo:
    
    # Header Section
    with gr.Column(elem_classes="main-container"):
        gr.HTML("""
        <div class="header-container">
            <h1 class="task-title">Chat Bot Project</h1>
            <div class="sub-title">Model Understanding & Evaluation System</div>
        </div>
        """)
        
        # Input Section
        with gr.Row():
            with gr.Column(scale=4):
                inp = gr.Textbox(
                    label="Enter Prompt", 
                    placeholder="E.g., Explain Quantum Computing in simple terms...",
                    lines=3,
                    elem_id="input-box"
                )
            with gr.Column(scale=1, min_width=150):
                btn = gr.Button("Analyze", variant="primary", size="lg")

        # Output Section
        gr.Markdown("### 📊 Analysis Results")
        
        out_html = gr.HTML(label="Response Visualization")
        
        with gr.Row():
            out_status = gr.Label(label="Status", num_top_classes=1)
            out_reason = gr.Label(label="Reasoning", num_top_classes=1)
        
        # Footer Section
        gr.HTML("""
        <div class="footer-container">
            Project Prepared by <span class="author-name">Yara Ali</span>
        </div>
        """)

    # Event Binding
    btn.click(fn=process_prompt, inputs=inp, outputs=[out_html, out_status, out_reason])

if __name__ == "__main__":
    demo.launch()