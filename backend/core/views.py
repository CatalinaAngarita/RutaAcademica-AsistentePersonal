from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


def index(request):
    """Vista para servir el frontend"""
    return render(request, 'index.html')

