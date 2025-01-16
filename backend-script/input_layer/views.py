import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Input
from utils.line_split import line_split
from utils.find_comment import find_comments


@csrf_exempt
def InputView(request, slug = None, pk = None, *args, **kwargs):
    """ 
    get code data from post request and store it the database
    for later processing
    get code data from get request
    """
    
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            code = data["code"]

            if not code:
                return JsonResponse({"error": "code field is required"}, status = 400)
            
            input = Input(
                code = code,
            )
            input.save(using = "default") # the using argument helps me decide on which db connections i would like to save default or replica or read_only

            data = {
                "id": input.id,
                "code": input.code,
                "created_at": input.created_at,
                "updated_at": input.updated_at
            }

            return JsonResponse(data, status = 200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status = 400)
        
    if request.method == "GET":
        if pk:
            if slug is None:
                try:
                    input = Input.objects.get(id = pk)
                    data = {
                        "id": input.id,
                        "code": input.code,
                        "created_at": input.created_at,
                        "updated_at": input.updated_at,
                    }
                    return JsonResponse(data, safe = False, status = 200)
                except Exception as e:
                    return JsonResponse({"error": str(e)}, status = 404)
            if slug == "line_split":
                try:
                    input = Input.objects.get(id = pk)
                    code = input.code
                    line_split_data = line_split(code)
                    return JsonResponse(line_split_data, safe = False, status = 200)
                except Exception as e:
                    return JsonResponse({"error": str(e)}, status = 404)
            if slug == "comment":
                try:
                    input = Input.objects.get(id = pk)
                    code = input.code 
                    line_split_data = line_split(code)
                    comments_data = find_comments(line_split_data)
                    return JsonResponse(comments_data, safe = False, status = 200)
                except Exception as e:
                    return JsonResponse({"error": str(e)}, status = 404)
        try:
            inputs = Input.objects.all()
            data = []
            for input in inputs:
                data.append({
                    "id": input.id,
                    "code": input.code,
                    "created_at": input.created_at,
                    "updated_at": input.updated_at,
                })
            return JsonResponse(data, safe = False,status = 200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status = 404)


""" @csrf_exempt
def retrieve(request, *args, **kwargs):
    print(request.method)
    if request.method == "GET":
        print("GET REQUEST")
        try:
            inputs = Input.objects.all()
            print(inputs)
            return JsonResponse({"data": "good life"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status = 400) """
    
""" 
def input(request, *args, **kwargs):
    
    if request.method == "POST":
        print(request.body)
        data = json.loads(request.body.decode("utf-8"))
        code = data["code"]
        return JsonResponse({"code": code})
    return JsonResponse({"error": "errorrr"})
"""
