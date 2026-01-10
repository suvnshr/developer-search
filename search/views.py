from django.shortcuts import render

from .helpers.search import perform_search_v2
from .helpers.theme import manage_theme

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
            "description": "High-level Python web framework encouraging rapid development and clean, pragmatic design.",
            "project_link": "https://github.com/django/django",
            "license_type": "BSD-3-Clause",
            "license_link": "https://github.com/django/django/blob/main/LICENSE",
            "copyright": "Copyright (c) Django Software Foundation",
        },
        "asgiref": {
            "description": "ASGI specifications and utilities for Python web applications.",
            "project_link": "https://github.com/django/asgiref",
            "license_type": "BSD-3-Clause",
            "license_link": "https://github.com/django/asgiref/blob/main/LICENSE",
            "copyright": "Copyright (c) Django Software Foundation",
        },
        "dj-database-url": {
            "description": "Utility to configure Django database settings from environment variables.",
            "project_link": "https://github.com/jazzband/dj-database-url",
            "license_type": "BSD-3-Clause",
            "license_link": "https://github.com/jazzband/dj-database-url/blob/main/LICENSE",
            "copyright": "Copyright (c) Jazzband contributors",
        },
        "django-heroku": {
            "description": "Django configuration wrapper for Heroku deployment.",
            "project_link": "https://github.com/heroku/django-heroku",
            "license_type": "MIT",
            "license_link": "https://github.com/heroku/django-heroku/blob/main/LICENSE",
            "copyright": "Copyright (c) Heroku",
        },
        "django-htmlmin": {
            "description": "HTML minification middleware for Django with HTML5 support.",
            "project_link": "https://github.com/cobrateam/django-htmlmin",
            "license_type": "BSD-2-Clause",
            "license_link": "https://github.com/cobrateam/django-htmlmin/blob/master/LICENSE",
            "copyright": "Copyright (c) django-htmlmin authors",
        },
        "whitenoise": {
            "description": "Static file serving for Python web apps with compression and caching support.",
            "project_link": "https://github.com/evansd/whitenoise",
            "license_type": "MIT",
            "license_link": "https://github.com/evansd/whitenoise/blob/main/LICENSE",
            "copyright": "Copyright (c) David Evans",
        },
        "gunicorn": {
            "description": "WSGI HTTP server for UNIX, designed for high concurrency and performance.",
            "project_link": "https://github.com/benoitc/gunicorn",
            "license_type": "MIT",
            "license_link": "https://github.com/benoitc/gunicorn/blob/master/LICENSE",
            "copyright": "Copyright (c) Benoît Chesneau",
        },
        "psycopg2": {
            "description": "PostgreSQL database adapter for Python.",
            "project_link": "https://github.com/psycopg/psycopg2",
            "license_type": "LGPL-3.0",
            "license_link": "https://github.com/psycopg/psycopg2/blob/master/LICENSE",
            "copyright": "Copyright (c) psycopg contributors",
        },
        "python-decouple": {
            "description": "Configuration management via environment variables.",
            "project_link": "https://github.com/henriquebastos/python-decouple",
            "license_type": "MIT",
            "license_link": "https://github.com/henriquebastos/python-decouple/blob/master/LICENSE",
            "copyright": "Copyright (c) Henrique Bastos",
        },
        "requests": {
            "description": "HTTP library for Python, designed to be simple and human-friendly.",
            "project_link": "https://github.com/psf/requests",
            "license_type": "Apache-2.0",
            "license_link": "https://github.com/psf/requests/blob/main/LICENSE",
            "copyright": "Copyright (c) Kenneth Reitz",
        },
        "urllib3": {
            "description": "Powerful HTTP client library used by requests.",
            "project_link": "https://github.com/urllib3/urllib3",
            "license_type": "MIT",
            "license_link": "https://github.com/urllib3/urllib3/blob/main/LICENSE.txt",
            "copyright": "Copyright (c) urllib3 contributors",
        },
        "certifi": {
            "description": "Mozilla’s curated collection of root certificates for SSL validation.",
            "project_link": "https://github.com/certifi/python-certifi",
            "license_type": "MPL-2.0",
            "license_link": "https://github.com/certifi/python-certifi/blob/master/LICENSE",
            "copyright": "Copyright (c) Kenneth Reitz",
        },
        "charset-normalizer": {
            "description": "Encoding detection library for Python.",
            "project_link": "https://github.com/Ousret/charset_normalizer",
            "license_type": "MIT",
            "license_link": "https://github.com/Ousret/charset_normalizer/blob/main/LICENSE",
            "copyright": "Copyright (c) Ousret",
        },
        "idna": {
            "description": "Internationalized Domain Names support for Python.",
            "project_link": "https://github.com/kjd/idna",
            "license_type": "BSD-3-Clause",
            "license_link": "https://github.com/kjd/idna/blob/master/LICENSE.md",
            "copyright": "Copyright (c) Kim Davies",
        },
        "beautifulsoup4": {
            "description": "HTML and XML parsing library for web scraping.",
            "project_link": "https://www.crummy.com/software/BeautifulSoup/",
            "license_type": "MIT",
            "license_link": "https://www.crummy.com/software/BeautifulSoup/bs4/doc/#license",
            "copyright": "Copyright (c) Leonard Richardson",
        },
        "soupsieve": {
            "description": "CSS selector library used by BeautifulSoup.",
            "project_link": "https://github.com/facelessuser/soupsieve",
            "license_type": "MIT",
            "license_link": "https://github.com/facelessuser/soupsieve/blob/main/LICENSE.md",
            "copyright": "Copyright (c) Isaac Muse",
        },
        "html5lib": {
            "description": "Standards-compliant HTML parsing library.",
            "project_link": "https://github.com/html5lib/html5lib-python",
            "license_type": "MIT",
            "license_link": "https://github.com/html5lib/html5lib-python/blob/master/LICENSE",
            "copyright": "Copyright (c) html5lib contributors",
        },
        "tldextract": {
            "description": "Separates subdomain, domain, and TLD using the Public Suffix List.",
            "project_link": "https://github.com/john-kurkowski/tldextract",
            "license_type": "BSD-3-Clause",
            "license_link": "https://github.com/john-kurkowski/tldextract/blob/master/LICENSE",
            "copyright": "Copyright (c) John Kurkowski",
        },
        "RapidFuzz": {
            "description": "High-performance fuzzy string matching library.",
            "project_link": "https://github.com/maxbachmann/RapidFuzz",
            "license_type": "MIT",
            "license_link": "https://github.com/maxbachmann/RapidFuzz/blob/main/LICENSE",
            "copyright": "Copyright (c) Max Bachmann",
        },
        "SerpApi": {
            "description": "API client for accessing search engine results.",
            "project_link": "https://github.com/serpapi/google-search-results-python",
            "license_type": "MIT",
            "license_link": "https://github.com/serpapi/google-search-results-python/blob/master/LICENSE",
            "copyright": "Copyright (c) SerpApi",
        },
        "google-api-python-client": {
            "description": "Official Python client library for Google APIs.",
            "project_link": "https://github.com/googleapis/google-api-python-client",
            "license_type": "Apache-2.0",
            "license_link": "https://github.com/googleapis/google-api-python-client/blob/main/LICENSE",
            "copyright": "Copyright (c) Google LLC",
        },
        "google-auth": {
            "description": "Google authentication library for Python.",
            "project_link": "https://github.com/googleapis/google-auth-library-python",
            "license_type": "Apache-2.0",
            "license_link": "https://github.com/googleapis/google-auth-library-python/blob/main/LICENSE",
            "copyright": "Copyright (c) Google LLC",
        },
        "protobuf": {
            "description": "Protocol Buffers serialization library.",
            "project_link": "https://github.com/protocolbuffers/protobuf",
            "license_type": "BSD-3-Clause",
            "license_link": "https://github.com/protocolbuffers/protobuf/blob/main/LICENSE",
            "copyright": "Copyright (c) Google",
        },
        "Materialize": {
            "description": "Modern responsive CSS framework based on Material Design.",
            "project_link": "https://github.com/Dogfalo/materialize",
            "license_type": "MIT",
            "license_link": "https://github.com/Dogfalo/materialize/blob/v1-dev/LICENSE",
            "copyright": "Copyright (c) Materialize",
        }
    }

    return render(
        request,
        "search/credits.html",
        {
            "projects": projects,
            **manage_theme(request, ""),
        },
    )
