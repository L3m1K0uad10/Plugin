import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from utils.translate_comment import get_comments_translation
#from utils.translate_comment2 import get_comments_translation


# Create your views here.

@csrf_exempt
def OutputView(request, pk = None, *args, **kwargs):
    
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))

            code = data.get("code")
            line_split = data.get("line_split")
            comments = data.get("comments")

            translated_comments = get_comments_translation(comments, line_split)

            data = {
                "translated_comments": translated_comments
            }

            return JsonResponse(data, status = 200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status = 400)

    if request.method == "GET":
        pass 
