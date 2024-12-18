import os
import google.generativeai as genai

genai.configure(api_key="AIzaSyDLZi6TiiFrH547uMVYZSx4Zpnl4_Yk7nM")


def gemini_api(word_to_search):
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 100,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
    )

    chat_session = model.start_chat(
        history=[
        ]
    )

    response = chat_session.send_message(word_to_search)

    print(response.text)