from django.urls import path
from . import views

urlpatterns = [
    path("", views.chatbot_page, name="chatbot-page"),
    path("api/send/", views.chatbot_send, name="chatbot-send"),
    path("api/new/", views.chatbot_new, name="chatbot-new"),
]
