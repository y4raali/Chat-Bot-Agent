Chat Bot Project — Model Understanding & Evaluation System

A Gradio-based web application that interfaces with the **Qwen 2.5 7B Instruct** model via the Hugging Face Inference API. Users can submit prompts and receive AI-generated responses along with an automatic quality evaluation of each response.

## ✨ Features

- 💬 **Live AI Chat** — Sends prompts to `Qwen/Qwen2.5-7B-Instruct` via Hugging Face's Inference API
- 📊 **Response Evaluation** — Automatically classifies each response as *Understood*, *Uncertain*, or *Error*
- 🎨 **Custom UI** 
- 🌐 **Bilingual Support** — Evaluation logic handles both English and Arabic prompts

## ⚙️ Requirements

- Python 3.8+
- A [Hugging Face account](https://huggingface.co/) with an API token

### Python Dependencies

Install all required packages with:

```bash
pip install gradio huggingface_hub
```
How to Run

1. Clone the Repository

2. Add Your Hugging Face API Token

Open `app.py` and replace the placeholder on line 8:

```python
HF_API_TOKEN = "InsertAPIkeyhere"
```

with your actual token:

```python
HF_API_TOKEN = "hf_xxxxxxxxxxxxxxxxxxxxxxxx"
```

> **Tip:** For better security, use an environment variable instead of hardcoding the token:
 3. Run the App
 4. Open in Browser

Once running, Gradio will provide a local host URL

Open it in your browser to start using the app.

To use:
1. Type any prompt into the **Enter Prompt** text box (English or Arabic)
2. Click the **Analyze** button
3. View the AI's response and the automatic evaluation status:
   - ✅ **Understood** — Clear, detailed response received
   - ⚠️ **Uncertain** — Response was too short or ambiguous
   - ❌ **Error** — A technical or API error occurred

## 👩‍💻 Author

Project prepared by **Yara Ali**
