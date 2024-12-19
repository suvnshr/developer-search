from django.shortcuts import render
from .helpers import perform_search_v2, manage_theme


# Create your views here.


def index(request):
    """The page where users can search"""

    page_index = None
    query = request.GET.get("q", "")

    try:
        page_index = int(request.GET.get("page", "0"))
    except ValueError:
        page_index = 0

    search_data = perform_search_v2(query, page_index)

    return render(
        request,
        "search/index.html",
        {
            "query": query,
            **search_data,
            **manage_theme(request, query, page_index),
        },
    )


def credits(request):
    """Credits to all the open source projects used in DevXplore"""

    # Data of each open source project included
    projects = {
        "Django": {
            "description": "Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design",
            "project_link": "https://github.com/django/django",
            "license_type": "BSD",
            "license_link": "https://github.com/django/django/blob/master/LICENSE.python",
            "copyright": "Copyright (c) Django Software Foundation and individual contributors.",
        },
        "Materialize": {
            "description": "Materialize, a CSS Framework based on Material Design",
            "project_link": "https://github.com/Dogfalo/materialize",
            "license_type": "MIT",
            "license_link": "https://github.com/Dogfalo/materialize/blob/v1-dev/LICENSE",
            "copyright": "Copyright (c) 2014-2019 Materialize",
        },
        "rapidfuzz": {
            "description": "Rapid fuzzy string matching in Python and C++ using the Levenshtein Distance",
            "project_link": "https://github.com/maxbachmann/rapidfuzz",
            "license_type": "MIT",
            "license_link": "https://github.com/maxbachmann/rapidfuzz/blob/master/LICENSE",
            "copyright": "Copyright © 2020 maxbachmann. Copyright © 2011 Adam Cohen",
        },
        "django-htmlmin": {
            "description": "django-html is an HTML minifier for Python, with full support for HTML 5",
            "project_link": "https://github.com/cobrateam/django-htmlmin",
            "license_type": "BSD",
            "license_link": "https://github.com/cobrateam/django-htmlmin/blob/master/LICENSE",
            "copyright": "Copyright (c) 2012, django-htmlmin authors. All rights reserved.",
        },
        "tldextract": {
            "description": "Accurately separate the TLD from the registered domain and subdomains of a URL, using the Public Suffix List.",
            "project_link": "https://github.com/john-kurkowski/tldextract",
            "license_type": "BSD",
            "license_link": "https://github.com/john-kurkowski/tldextract/blob/master/LICENSE",
            "copyright": "Copyright (c) 2019, John Kurkowski. All rights reserved.",
        },
        "python-decouple": {
            "description": "Decouple helps you to organize your settings so that you can change parameters without having to redeploy your app.",
            "project_link": "https://github.com/henriquebastos/python-decouple/",
            "license_type": "MIT",
            "license_link": "https://github.com/henriquebastos/python-decouple/blob/master/LICENSE",
            "copyright": "Copyright (c) 2013 Henrique Bastos",
        },
        "gunicorn": {
            "description": "gunicorn 'Green Unicorn' is a WSGI HTTP Server for UNIX, fast clients and sleepy applications",
            "project_link": "https://github.com/benoitc/gunicorn",
            "license_type": "MIT",
            "license_link": "https://github.com/benoitc/gunicorn/blob/master/LICENSE",
            "copyright": "2009-2018 (c) Benoît Chesneau. 2009-2015 (c) Paul J. Davis ",
        },
        "SerpApi": {
            "description": "SerpApi is a real-time API to access search engine result pages (SERPs).",
            "project_link": "https://github.com/serpapi/google-search-results-python",
            "license_type": "MIT",
            "license_link": "https://github.com/serpapi/google-search-results-python/blob/master/LICENSE",
            "copyright": "Copyright (c) 2020 SerpApi, LLC",
        },
    }

    return render(
        request,
        "search/credits.html",
        {
            "projects": projects,
            **manage_theme(request, ""),
        },
    )
