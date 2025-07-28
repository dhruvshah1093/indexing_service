from django.urls import path
from .views import PromptView

urlpatterns = [
    path("prompt/", PromptView.as_view(), name="create-prompt"),
    path("prompt/<uuid:pk>/", PromptView.as_view(), name="get-prompt"),
]
