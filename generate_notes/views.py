import os
import markdown as md
from django.shortcuts import render, get_object_or_404
from file_upload.models import UploadedFile
from .models import GeneratedNote
from dotenv import load_dotenv
from google import generativeai as genai

# Load .env and configure Gemini
load_dotenv()
print(f"DEBUG: Loaded Key Status: {os.getenv('GENAI_API_KEY')[:5] if os.getenv('GENAI_API_KEY') else 'KEY NOT FOUND'}...")
genai.configure(api_key=os.getenv("GENAI_API_KEY") or "YOUR_API_KEY_HERE")

def generate_notes_from_text(text):
    """Generate summarized study notes using Gemini API."""
    try:
        # ✅ Correct model name for version 0.8.5
        model = genai.GenerativeModel("gemini-2.5-flash")

        # Enhanced prompt for generating structured exam notes
        prompt = f"""
        Create comprehensive, well-structured study notes from the following content. Format your response with:
        
        1. **Main Topics** - Use clear headings
        2. **Key Points** - Use bullet points (•) for important information
        3. **Definitions** - Highlight important terms and their meanings
        4. **Examples** - Include relevant examples where applicable
        5. **Summary** - End with a brief summary of key takeaways
        
        Make the notes exam-ready, concise, and easy to understand. Use proper formatting with headings, bullet points, and numbered lists where appropriate.
        
        Content to summarize:
        {text}
        """

        # Generate response
        response = model.generate_content(prompt)
        print("Gemini response:", response)  # Debugging info

        # Extract text safely
        if hasattr(response, 'text') and response.text:
            return response.text.strip()
        elif hasattr(response, 'candidates') and response.candidates:
            return response.candidates[0].content.parts[0].text.strip()
        else:
            return "No notes generated. Try again."
    except Exception as e:
        print("Gemini Error:", e)
        return None


def generate_notes(request, uploaded_file_id):
    uploaded_file = get_object_or_404(UploadedFile, id=uploaded_file_id)
    text = uploaded_file.extracted_text

    # 1. Handle the case where the text is EMPTY
    if not text or len(text) < 10:
        # ✅ Correctly returns an HttpResponse object with the error message
        return render(request, "generate_notes/notes.html", {
            "error": "CRITICAL ERROR: No text found in the uploaded file's extracted_text field. Check the file upload and extraction step.",
            "uploaded_file": uploaded_file
        })

    # 2. If text is present, proceed with note generation (your original logic)
    notes = generate_notes_from_text(text)

    if notes and notes != "No notes generated. Try again.":
        GeneratedNote.objects.create(uploaded_file=uploaded_file, notes=notes)
        notes_html = md.markdown(notes, extensions=['tables', 'fenced_code', 'nl2br'])
        return render(request, "generate_notes/notes.html", {"notes": notes_html, "uploaded_file": uploaded_file})
    else:
        # This handles both API failure and the "No notes generated" fallback from the Gemini function
        return render(request, "generate_notes/notes.html", {
            "error": "Error generating notes (API failure or empty response). Please try again.",
            "uploaded_file": uploaded_file
        })