
from django.shortcuts import render

def custom_404(request, exception):
    return render(request, "404.html", status=404)

from django.http import HttpResponseNotFound

def test_404(request):
    return HttpResponseNotFound(render(request, "404.html"))