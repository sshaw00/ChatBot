import openai
import gradio as gr
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()
print(gr.__version__)

openai.api_key = os.getenv("API")

# Initialize messages within the function to avoid retaining state between calls
def CustomChatGPT(user_input, messages=None):
    if messages is None:
        messages = [{"role": "system", "content": "Creative teacher specialising in Design Thinking on Project Based Learning"}]
    
    messages.append({"role": "user", "content": user_input})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    ChatGPT_reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": ChatGPT_reply})
    return ChatGPT_reply

# Use gradio instead of gr
demo = gr.Interface(fn=CustomChatGPT, inputs="text", outputs="text", title="Custom ChatGPT")

# Get the port from the environment variable, or default to 7861
port = int(os.getenv("PORT", 7861))

# Specify the host and port for the Gradio app
demo.launch(share=True,server_name="0.0.0.0", server_port=port)
