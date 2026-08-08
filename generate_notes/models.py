from django.db import models
# Import the model from the file_upload app
from file_upload.models import UploadedFile 

class GeneratedNote(models.Model):
    # Links the generated notes back to the original file
    # If the file is deleted, the notes are also deleted (models.CASCADE)
    uploaded_file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE)
    
    # Field to store the output from the Gemini API
    notes = models.TextField()
    
    # Timestamp
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notes for {self.uploaded_file.original_name}"