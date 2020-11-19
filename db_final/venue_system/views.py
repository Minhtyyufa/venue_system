from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from rest_framework import viewsets
from .serializers import RoleSerializer
from .models import Role
from rest_framework.decorators import api_view, action
from rest_framework.response import Response

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all().order_by("role")
    serializer_class = RoleSerializer

    @action(detail=False, url_path = "list_roles", url_name="list_roles")
    def list_roles(self, request):
        print(request)
        queryset = Role.objects.all().order_by("role")
        serializer = RoleSerializer(queryset, many =True)
        return Response(serializer.data)

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
