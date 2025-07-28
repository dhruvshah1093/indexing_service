from rest_framework import serializers
from .models import PromptEntry

class PromptEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = PromptEntry
        fields = "__all__"
