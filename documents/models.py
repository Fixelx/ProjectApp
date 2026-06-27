from django.db import models
from projects.models import Project
import os

def document_upload_path(instance, filename):
    return f"projects/{instance.project.id}/documents/{filename}"

class DocumentCategory(models.Model):
    name = models.CharField(max_length=120, unique=True)

    class Meta:
        verbose_name = "Dokumentenkategorie"
        verbose_name_plural = "Dokumentenkategorien"
        ordering = ["name"]

    def __str__(self):
        return self.name

class Document(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="documents")
    category = models.ForeignKey(DocumentCategory, on_delete=models.CASCADE, verbose_name="Kategorie")
    title = models.CharField(max_length=255, verbose_name="Name")
    file = models.FileField(upload_to=document_upload_path, verbose_name="Datei")
    uploaded_by = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def extension(self):
        return os.path.splitext(self.file.name)[1].lower()

    def __str__(self):
        return self.title