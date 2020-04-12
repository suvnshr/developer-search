from django.http import HttpResponse
from django.shortcuts import render
from .helpers import get_current_theme, get_requested_theme, set_new_theme, get_theme_url
from .helpers import perform_search
from urllib.parse import urlencode

# Create your views here.


def index(request):

    url_params = {}
    query = request.GET.get("q", "")

    current_theme = get_current_theme(request)
    requested_theme = get_requested_theme(request)

    if requested_theme and requested_theme != current_theme:
        set_new_theme(request, requested_theme)
        current_theme = requested_theme

    results, limit_reached = perform_search(query)

    light_theme_url = get_theme_url(request, query, "light")
    dark_theme_url = get_theme_url(request, query, "dark")

    return render(request, "search/index.html", {
        "query": query,
        "results": results,
        "limit_reached": limit_reached,
        "theme": current_theme,
        "light_theme_url": light_theme_url,
        "dark_theme_url": dark_theme_url,
    })
