from django.shortcuts import render, redirect
import io
from .forms import UploadForm
from .models import UploadedFile
import PyPDF2

def upload_file(request):
    text = None
    error = None
    uploaded_file_instance = None

    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)
        action = request.POST.get('action')

        if form.is_valid():
            uploaded_file = form.cleaned_data['file']

            uploaded_file_instance = UploadedFile.objects.create(
                file=uploaded_file,
                original_name=uploaded_file.name
            )

            try:
                uploaded_file_instance.file.open()
                file_data = uploaded_file_instance.file.read()
                pdf_file = io.BytesIO(file_data)

                reader = PyPDF2.PdfReader(pdf_file)
                text = "\n\n".join([p.extract_text() or "" for p in reader.pages]).strip()

                uploaded_file_instance.extracted_text = text
                uploaded_file_instance.save()

                if action == 'quiz':
                    return redirect('generate_quiz:generate_quiz', uploaded_file_id=uploaded_file_instance.id)
                else:
                    return redirect('generate_notes:generate_notes', uploaded_file_id=uploaded_file_instance.id)

            except Exception as e:
                print(f"PDF extraction failed: {e}")
                error = "PDF extraction error. Please ensure the file is a readable PDF."

            finally:
                if uploaded_file_instance and uploaded_file_instance.file:
                    uploaded_file_instance.file.close()
    else:
        form = UploadForm()

    all_files = UploadedFile.objects.all().order_by('-uploaded_at')

    return render(request, "file_upload/upload.html", {
        "form": form,
        "text": text,
        "error": error,
        "uploaded_files": all_files,
        "uploaded_file": uploaded_file_instance
    })
