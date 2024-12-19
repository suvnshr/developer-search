import tldextract
from decouple import config
from rapidfuzz import fuzz
from urllib.parse import urlencode
from . import constants
from serpapi import GoogleSearch


def search_url_with_page_index(query, page):
    """returns url for search results of next or previous page"""

    return f"?q={query}&page={page}"


def manage_theme(request, query, page_index=None):
    """manages theme related tasks in each view:
    - setting & unsetting of session variable `theme`
    - url for the theme, opposite of the theme currently being used
    """

    # the current value of session variable
    current_theme = get_current_theme(request)

    # the theme requested by user
    requested_theme = get_requested_theme(request)

    # check whether a theme is requested
    # and the requested theme is different from the currently set theme
    if requested_theme and requested_theme != current_theme:
        set_new_theme(request, requested_theme)
        current_theme = requested_theme

    # url to set light theme as the current theme
    light_theme_url = get_theme_url(request, query, "light", page_index)

    # url to set dark theme as the current theme
    dark_theme_url = get_theme_url(request, query, "dark", page_index)

    # this data will be passed in context of each view
    return {
        "theme": current_theme,
        "light_theme_url": light_theme_url,
        "dark_theme_url": dark_theme_url,
        # whether the users has changed the theme using the button present on the site
        # then user's system theme preference will no be supported
        "theme_session_set": "true" if request.session.get("theme", None) else "false",
    }


def keyword_in_search(search_item, keywords=(), must_contain_all=False):
    """whether `keyword` is present in `search_item`"""

    link = search_item["link"]
    title = search_item["title"]
    snippet = search_item["snippet"]
    filter_func = all if must_contain_all else any

    for information in (link, title, snippet):

        if filter_func(
            # normal search
            keyword.lower() in information.lower()
            for keyword in keywords
        ):
            return True

        if filter_func(
            # fuzzy search
            fuzz.WRatio(keyword, information, score_cutoff=90)
            for keyword in keywords
        ):

            return True

    return False


def domain_in_search(search_item, domains=()):
    """whether `search_item` is a result from provided `domains`"""

    link = search_item["link"]

    if len(domains) == 0:
        # if no domains are provided then return True
        # i.e: Let it appear on search

        return True

    else:
        for domain in domains:
            required_domain = tldextract.extract(domain).domain
            search_result_domain = tldextract.extract(link).domain

            if required_domain == search_result_domain:
                return True


def classify_search(search_items, titles_and_details={}):
    """gives a dict which contains list of `search_items` in their respective categories"""

    search_data = {
        "all": search_items,
    }

    for title, details in titles_and_details.items():

        keywords = details.get("keywords", ())
        domains = details.get("domains", ())
        must_contain_all_keywords = details.get("must_contain_all_keywords", False)

        def filter_domains(search_item):
            """to filter all the `search_item`s which are from `domains`"""

            return domain_in_search(search_item, domains)

        def filter_keywords(search_item):
            """to filter all the `search_item`s which contains `keyword`"""
            return keyword_in_search(
                search_item, keywords, must_contain_all=must_contain_all_keywords
            )

        # filtering all results which contains `keyword`
        keywords_filtered = list(filter(filter_keywords, search_items))

        # filtering all results which are from `domain`

        domains_filtered = list(filter(filter_domains, search_items))

        search_data[title] = domains_filtered + keywords_filtered

    return search_data


def theme_filter(theme):
    """filter the theme string, of something other than light or dark is provided,
    then it returns light"""

    return {
        "light": "light",
        "dark": "dark",
    }.get(theme, "light")


def get_current_theme(request):
    """returns the value of current session variable 'theme'"""

    return request.session.get("theme")


def get_requested_theme(request):
    """
    gets the currently requested theme,
    by fetching the value of query parameter `theme`
    """

    return request.GET.get("theme", None)


def set_new_theme(request, theme):
    """sets the session variable `theme` to the desired value"""

    theme = theme_filter(theme)
    request.session["theme"] = theme
    request.session.set_expiry(43800)


def get_theme_url(request, query, theme, page_index=None):
    """returns the url to set a specific theme"""

    # remove `q` parameter if it is not mentioned
    url_dict = {"q": query, "theme": theme} if query else {"theme": theme}

    # add `page` parameter to url
    if page_index:
        url_dict["page"] = page_index

    return request.path + "?" + urlencode(url_dict)


def call_serpapi(search_query, page_index):

    api_response = {}

    try:
        serpapi_params = {
            "api_key": config("SERP_API_KEY"),
            "engine": "google",
            "q": search_query,
            "google_domain": "google.com",
            "safe": "active",
            "uds": "technology,code,engineer,software,ai",
            "num": "10",
            "start": page_index,
        }

        search = GoogleSearch(serpapi_params)
        api_response = search.get_dict()

        error_from_serpapi = api_response.get("error")

        if error_from_serpapi:

            if "run out of searches" in error_from_serpapi:
                api_response = {
                    "error_code": 429,
                }

            elif (
                "Google hasn't returned any results for this query."
                in error_from_serpapi
            ):
                api_response = {
                    "error_code": 400,
                }

            else:
                api_response = {
                    "error_code": 500,
                }

    except Exception as e:
        api_response = {
            "error_code": 500,
        }

    return api_response


# Peform search using serpapi
def perform_search_v2(search_query, page_index=0):

    has_prev_page = False
    has_next_page = False
    limit_reached = False
    error_occured = False

    prev_page_page_index = None
    next_page_page_index = None

    prev_page_url = None
    next_page_url = None

    results = {}

    if search_query:

        api_response = call_serpapi(search_query, page_index)
        api_response_err_code = api_response.get("error_code")

        if api_response_err_code == 429:
            api_response = {}
            limit_reached = True

        elif api_response_err_code == 400:
            api_response = {}

        elif api_response_err_code == 500:
            api_response = {}
            error_occured = True

        else:
            pagination = api_response.get("pagination")
            has_prev_page = pagination.get("previous")
            has_next_page = pagination.get("next")

            if has_prev_page:
                prev_page_page_index = page_index - 1 if page_index > 0 else 1
                prev_page_url = search_url_with_page_index(
                    search_query, prev_page_page_index
                )

            if has_next_page:
                next_page_page_index = page_index + 1 if page_index > -1 else 1
                next_page_url = search_url_with_page_index(
                    search_query, next_page_page_index
                )

        search_items = api_response.get("organic_results", [])

        results = classify_search(search_items, constants.SEARCH_CATEGORY_DATA)

    return {
        "results": results,
        "limit_reached": limit_reached,
        "has_next_page": has_next_page,
        "has_prev_page": has_prev_page,
        "prev_page_url": prev_page_url,
        "next_page_url": next_page_url,
        "error_occured": error_occured,
    }
