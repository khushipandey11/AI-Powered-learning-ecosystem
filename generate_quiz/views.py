import os
import json
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from file_upload.models import UploadedFile
from .models import GeneratedQuiz, QuizQuestion
from dotenv import load_dotenv
from google import generativeai as genai

# Load .env and configure Gemini
load_dotenv()
genai.configure(api_key=os.getenv("GENAI_API_KEY") or "YOUR_API_KEY_HERE")

def generate_quiz_from_text(text):
    """Generate a 10-question quiz using Gemini API."""
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        
        prompt = f"""
        Create a 10-question multiple choice quiz based on the following content. 
        Format your response as a JSON array with exactly this structure:
        [
            {{
                "question": "Question text here?",
                "options": {{
                    "A": "Option A text",
                    "B": "Option B text", 
                    "C": "Option C text",
                    "D": "Option D text"
                }},
                "correct_answer": "A"
            }}
        ]
        
        Make sure:
        - Each question tests understanding of the content
        - All 4 options are plausible but only one is correct
        - Questions cover different aspects of the material
        - Return valid JSON only, no additional text
        
        Content: {text[:4000]}
        """
        
        response = model.generate_content(prompt)
        
        if hasattr(response, 'text') and response.text:
            quiz_text = response.text.strip()
        elif hasattr(response, 'candidates') and response.candidates:
            quiz_text = response.candidates[0].content.parts[0].text.strip()
        else:
            return None
            
        # Clean up the response to extract JSON
        if quiz_text.startswith('```json'):
            quiz_text = quiz_text[7:]
        if quiz_text.endswith('```'):
            quiz_text = quiz_text[:-3]
        quiz_text = quiz_text.strip()
        
        # Parse JSON
        quiz_data = json.loads(quiz_text)
        return quiz_data
        
    except Exception as e:
        print("Quiz Generation Error:", e)
        return None

def generate_quiz(request, uploaded_file_id):
    uploaded_file = get_object_or_404(UploadedFile, id=uploaded_file_id)
    text = uploaded_file.extracted_text
    
    # Check if text exists
    if not text or len(text) < 10:
        return render(request, "generate_quiz/quiz.html", {
            "error": "No text found in the uploaded file. Please upload a valid PDF with text content.",
            "uploaded_file": uploaded_file
        })
    
    # Generate quiz
    quiz_data = generate_quiz_from_text(text)
    
    if quiz_data and isinstance(quiz_data, list) and len(quiz_data) > 0:
        # Save quiz to database
        generated_quiz = GeneratedQuiz.objects.create(
            uploaded_file=uploaded_file,
            quiz_data=quiz_data
        )
        
        # Save individual questions
        for i, question_data in enumerate(quiz_data):
            QuizQuestion.objects.create(
                quiz=generated_quiz,
                question_text=question_data['question'],
                option_a=question_data['options']['A'],
                option_b=question_data['options']['B'],
                option_c=question_data['options']['C'],
                option_d=question_data['options']['D'],
                correct_answer=question_data['correct_answer']
            )
        
        return render(request, "generate_quiz/quiz.html", {
            "quiz_data": quiz_data,
            "uploaded_file": uploaded_file,
            "quiz_id": generated_quiz.id
        })
    else:
        return render(request, "generate_quiz/quiz.html", {
            "error": "Error generating quiz. Please try again.",
            "uploaded_file": uploaded_file
        })

def export_quiz(request, quiz_id):
    """Export quiz as JSON or TXT file"""
    quiz = get_object_or_404(GeneratedQuiz, id=quiz_id)
    format_type = request.GET.get('format', 'json')
    
    if format_type == 'txt':
        # Generate text format
        content = f"Quiz for: {quiz.uploaded_file.original_name}\n"
        content += "=" * 50 + "\n\n"
        
        for i, question_data in enumerate(quiz.quiz_data, 1):
            content += f"Question {i}: {question_data['question']}\n"
            content += f"A) {question_data['options']['A']}\n"
            content += f"B) {question_data['options']['B']}\n"
            content += f"C) {question_data['options']['C']}\n"
            content += f"D) {question_data['options']['D']}\n"
            content += f"Correct Answer: {question_data['correct_answer']}\n\n"
        
        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="quiz_{quiz.uploaded_file.original_name}_{quiz.id}.txt"'
        return response
    
    else:  # Default to JSON
        export_data = {
            "file_name": quiz.uploaded_file.original_name,
            "created_at": quiz.created_at.isoformat(),
            "questions": quiz.quiz_data
        }
        
        response = HttpResponse(
            json.dumps(export_data, indent=2),
            content_type='application/json'
        )
        response['Content-Disposition'] = f'attachment; filename="quiz_{quiz.uploaded_file.original_name}_{quiz.id}.json"'
        return response
