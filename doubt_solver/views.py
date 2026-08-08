import os
from django.shortcuts import render
from django.http import JsonResponse
from .models import Doubt
from dotenv import load_dotenv
from google import generativeai as genai

# Load .env and configure Gemini
load_dotenv()
genai.configure(api_key=os.getenv("GENAI_API_KEY") or "YOUR_API_KEY_HERE")

def solve_doubt_with_ai(question):
    """Solve doubt using Gemini AI."""
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        prompt = f"Please provide a clear, detailed explanation for the following question or doubt: {question}"
        
        response = model.generate_content(prompt)
        
        if hasattr(response, 'text') and response.text:
            return response.text.strip()
        elif hasattr(response, 'candidates') and response.candidates:
            return response.candidates[0].content.parts[0].text.strip()
        else:
            return "Sorry, I couldn't generate an answer. Please try again."
    except Exception as e:
        print("Gemini Error:", e)
        return "Sorry, there was an error processing your question. Please try again."

def doubt_solver(request):
    """Main doubt solver view."""
    if request.method == 'POST':
        question = request.POST.get('question', '').strip()
        
        if question:
            # Generate answer using AI
            answer = solve_doubt_with_ai(question)
            
            # Save to database
            doubt = Doubt.objects.create(question=question, answer=answer)
            
            return render(request, 'doubt_solver/doubt_result.html', {
                'question': question,
                'answer': answer
            })
        else:
            return render(request, 'doubt_solver/doubt_form.html', {
                'error': 'Please enter a question.'
            })
    
    return render(request, 'doubt_solver/doubt_form.html')
