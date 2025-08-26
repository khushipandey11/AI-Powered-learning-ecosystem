import os
import openai

def generate_notes(text):
    prompt = f"Summarize the following text into clear , concise study notes for exam prep : \n\n\n {text}"
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Or "gpt-4" if you have access
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    
    return response.choices[0].message["content"]