
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound

@login_required
def custom_404(request, exception):
    return render(request, "404.html", status=404)

@login_required
def test_404(request):
    return HttpResponseNotFound(render(request, "404.html"))