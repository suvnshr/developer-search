from urllib.parse import urlencode

"""
Theme Management Module

Provides utilities for managing light/dark theme preferences.
Handles theme switching via query parameters, persists preferences in session storage,
and generates URLs for theme toggling while preserving other query parameters.
"""


def manage_theme(request, query, page_index=None):
    """
    Manages theme-related tasks for a view, including session handling and URL generation.

    Args:
        request: Django HttpRequest object containing session and GET parameters
        query: Current search query string to preserve in theme URLs
        page_index: Current pagination page number (optional)

    Returns:
        dict: Context dictionary with theme, light_theme_url, dark_theme_url, and theme_session_set
    """
    current_theme = get_current_theme(request)
    requested_theme = get_requested_theme(request)

    if requested_theme and requested_theme != current_theme:
        set_new_theme(request, requested_theme)
        current_theme = requested_theme

    light_theme_url = get_theme_url(request, query, "light", page_index)
    dark_theme_url = get_theme_url(request, query, "dark", page_index)

    return {
        "theme": current_theme,
        "light_theme_url": light_theme_url,
        "dark_theme_url": dark_theme_url,
        "theme_session_set": "true" if request.session.get(
            "theme",
            None) else "false",
    }


def theme_filter(theme):
    """
    Validates and normalizes theme values to "light" or "dark".

    Args:
        theme: Theme string to validate

    Returns:
        str: Validated theme string ("light" or "dark"), defaults to "light"
    """
    return {
        "light": "light",
        "dark": "dark",
    }.get(theme, "light")


def get_current_theme(request):
    """
    Retrieves the currently active theme from the session.

    Args:
        request: Django HttpRequest object

    Returns:
        str or None: Current theme value
    """
    return request.session.get("theme")


def get_requested_theme(request):
    """
    Extracts the theme value from the request's query parameters.

    Args:
        request: Django HttpRequest object

    Returns:
        str or None: Requested theme value from query parameter
    """
    return request.GET.get("theme", None)


def set_new_theme(request, theme):
    """
    Persists a new theme preference to the user's session.

    Args:
        request: Django HttpRequest object
        theme: Desired theme value
    """
    theme = theme_filter(theme)
    request.session["theme"] = theme
    request.session.set_expiry(43800)


def get_theme_url(request, query, theme, page_index=None):
    """
    Constructs a URL for switching themes while preserving current page state.

    Args:
        request: Django HttpRequest object
        query: Search query string to preserve
        theme: Target theme value
        page_index: Current pagination page number (optional)

    Returns:
        str: Complete URL with path and encoded query parameters
    """
    url_dict = {"q": query, "theme": theme} if query else {"theme": theme}
    if page_index:
        url_dict["page"] = page_index
    return request.path + "?" + urlencode(url_dict)
