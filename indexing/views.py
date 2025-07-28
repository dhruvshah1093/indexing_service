import uuid, json
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PromptEntry
from .serializers import PromptEntrySerializer
from .storage_utils import upload_file_to_s3
from core.kafka_utils.producer import KafkaProducerWrapper

producer = KafkaProducerWrapper()

class PromptView(APIView):
    def post(self, request):
        prompt = request.data.get("prompt")
        group_id = request.data.get("group_id")
        file = request.FILES.get("file")

        if not prompt:
            return Response({"error": "Prompt is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Save file locally (can extend to S3)
        attachment_location = None
        if file:
            attachment_location = upload_file_to_s3(file, "prompt_files")

        # Create DB entry
        entry = PromptEntry.objects.create(
            prompt=prompt,
            group_id=group_id or None,
            attachment_location=attachment_location,
            result={"status": "processing"}
        )

        serializer = PromptEntrySerializer(entry)

        # Cache the prompt for faster retrieval
        cache.set(f"prompt:{entry.id}", serializer.data, timeout=3600)

        # Produce Kafka message
        producer.send(
            topic="prompt_created",
            key=str(entry.id),
            value=json.dumps(serializer.data)
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, pk=None):
        """Retrieve a prompt by ID (check cache first)"""
        if not pk:
            return Response({"error": "Prompt ID required"}, status=status.HTTP_400_BAD_REQUEST)

        cached_prompt = cache.get(f"prompt:{pk}")
        if cached_prompt:
            return Response(cached_prompt, status=status.HTTP_200_OK)

        try:
            entry = PromptEntry.objects.get(pk=pk)
        except PromptEntry.DoesNotExist:
            return Response({"error": "Prompt not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PromptEntrySerializer(entry)
        cache.set(f"prompt:{pk}", serializer.data, timeout=3600)
        return Response(serializer.data, status=status.HTTP_200_OK)
