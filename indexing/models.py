import uuid
from django.db import models

class PromptEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group_id = models.UUIDField(null=True, blank=True)
    prompt = models.TextField()
    attachment_location = models.TextField(null=True, blank=True)
    result = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "prompt_entries"

    def __str__(self):
        return f"{self.prompt[:50]} ({self.id})"
