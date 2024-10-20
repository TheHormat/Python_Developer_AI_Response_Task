import google.generativeai as genai
import os

# Configuring the Google AI API
genai.configure(api_key="SECRET_KEY")

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    system_instruction="precise and concise outputs",
)

def generate_ai_response(comment_content: str):
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    f"Write a response related to this comment: '{comment_content}'",
                ],
            },
        ]
    )
    response = chat_session.send_message(f"Respond to the comment: {comment_content}")
    return response.text