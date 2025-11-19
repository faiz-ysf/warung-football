from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.models import User

import json


@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = None
        password = None
        
        # Try to parse as JSON first
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
        except json.JSONDecodeError:
            # If JSON parsing fails, assume form-encoded data
            username = request.POST.get('username')
            password = request.POST.get('password')

        if not all([username, password]):
            return JsonResponse({
                "status": False,
                "message": "Missing required fields: username and password."
            }, status=400)
    
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                # Login status successful.
                return JsonResponse({
                    "username": user.username,
                    "status": True,
                    "message": "Login successful!"
                    # Add other data if you want to send data to Flutter.
                }, status=200)
            else:
                return JsonResponse({
                    "status": False,
                    "message": "Login failed, account is disabled."
                }, status=401)

        else:
            return JsonResponse({
                "status": False,
                "message": "Login failed, please check your username or password."
            }, status=401)
@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"status": False, "message": "Invalid JSON payload."}, status=400)

        username = data.get('username')
        password1 = data.get('password1')
        password2 = data.get('password2')

        if not all([username, password1, password2]):
            return JsonResponse({
                "status": False,
                "message": "Missing required fields: username, password1, and password2."
            }, status=400)
        
        # Check if the passwords match
        if password1 != password2:
            return JsonResponse({
                "status": False,
                "message": "Passwords do not match."
            }, status=400)
        
        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                "status": False,
                "message": "Username already exists."
            }, status=400)
        
        # Create the new user
        user = User.objects.create_user(username=username, password=password1)
        user.save()
        
        return JsonResponse({
            "username": user.username,
            "status": 'success',
            "message": "User created successfully!"
        }, status=200)
    
    else:
        return JsonResponse({
            "status": False,
            "message": "Invalid request method."
        }, status=400)

@csrf_exempt
def logout(request):
    username = request.user.username
    try:
        auth_logout(request)
        return JsonResponse({
            "username": username,
            "status": True,
            "message": "Logged out successfully!"
        }, status=200)
    except:
        return JsonResponse({
            "status": False,
            "message": "Logout failed."
        }, status=401)
