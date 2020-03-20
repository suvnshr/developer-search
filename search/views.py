from django.http import HttpResponse
from django.shortcuts import render

from .helpers import perform_search

# Create your views here.


def index(request):

    query = request.GET.get("q", "")
    results, limit_reached = perform_search(query)

    return render(request, "search/index.html", {
        "query": query,
        "results": results,
        "limit_reached": limit_reached
    })
