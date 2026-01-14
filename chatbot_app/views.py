from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .llm_service import ai_news_bot

def chatbot_page(request):
    """Render the main chat widget page."""
    return render(request, "chatbot_app/chat_widget.html")


@csrf_exempt
def chatbot_send(request):
    """Handle AJAX POST request for sending messages."""
    if request.method == "POST":
        import json
        data = json.loads(request.body.decode("utf-8"))
        message = data.get("message", "").strip()
        if not message:
            return JsonResponse({"success": False, "assistant_response": "Please type a message."})
        response = ai_news_bot(message)
        return JsonResponse({"success": True, "assistant_response": response})
    return JsonResponse({"success": False, "assistant_response": "Invalid request."})


@csrf_exempt
def chatbot_new(request):
    """Reset chat history (optional)."""
    if request.method == "POST":
        return JsonResponse({"success": True})
    return JsonResponse({"success": False})
