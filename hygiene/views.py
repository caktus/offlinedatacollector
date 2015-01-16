from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'hygiene/index.html', {})


def connection_test(request):
    return HttpResponse(status=204)
