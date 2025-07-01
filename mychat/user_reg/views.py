from django.shortcuts import render
import json
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .serializers import UserListSerializer
from rest_framework.generics import ListAPIView


# Create your views here.
def register(request):
    if request.user.is_authenticated:
            return redirect(reverse("home"))
    if request.method=="POST":
        data = json.loads(request.body)
        username = data.get('username')
        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already taken"}, status=400)
        try:
            user = User.objects.create_user(first_name=data.get('firstName'),last_name=data.get('lastName'),username=data.get('username'),password=data.get("password"))
            login(request,user)
            return JsonResponse({"success": True})
            return redirect(reverse("home"))
        except Exception as err:
            return JsonResponse({"error":str(err)}, status=500)
    else:
        return render(request,"register_page.html")

def login_v(request):
    if request.method=='POST':
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"success": False, "error": "Invalid user"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    else:
        if request.user.is_authenticated:
            return redirect(reverse("home"))
        else:
            return render(request,'login_page.html')
        


class UserListView(ListAPIView):
    queryset = User.objects.select_related('profile')
    serializer_class = UserListSerializer
