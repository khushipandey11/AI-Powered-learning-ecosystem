from django.db import models

# Create your models here.
class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    original_name = models.CharField(max_length=512)
    extracted_text = models.TextField(blank=True, null=True)  # NEW FIELD
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"File: {self.original_name} (ID: {self.id})"