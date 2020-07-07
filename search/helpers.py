import tldextract
from decouple import config
from rapidfuzz import fuzz
from googleapiclient.discovery import build
from urllib.parse import urlencode
from django.conf import settings
import requests


def search_url_with_start_index(query, start):
    """ returns url for search results of next or previous page """

    return f"?q={query}&start={start}"

def manage_theme(request, query, start_index):

    """ manages theme related tasks in each view:
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
    light_theme_url = get_theme_url(request, query, "light", start_index)

    # url to set dark theme as the current theme
    dark_theme_url = get_theme_url(request, query, "dark", start_index)

    # this data will be passed in context of each view
    return {
        "theme": current_theme,
        "light_theme_url": light_theme_url,
        "dark_theme_url": dark_theme_url,
        
        # whether the users has changed the theme using the button present on the site
        # then user's system theme preference will no be supported
        "theme_session_set": "true" if request.session.get("theme", None) else "false"
    }



def keyword_in_search(search_item, keywords=(), must_contain_all=False):
    """ whether `keyword` is present in `search_item` """

    link = search_item['link']
    title = search_item['title']
    snippet = search_item['snippet']
    filter_func = all if must_contain_all else any

    for information in (link, title, snippet):

        if filter_func(
            # normal search
            keyword.lower() in information.lower() for keyword in keywords
        ):
            return True

        if filter_func(
            # fuzzy search
            fuzz.WRatio(keyword, information, score_cutoff=90) for keyword in keywords
        ):

            return True

    return False


def domain_in_search(search_item, domains=()):
    """ whether `search_item` is a result from provided `domains`  """

    link = search_item['link']

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
    """ gives a dict which contains list of `search_items` in their respective categories"""

    search_data = {
        'all': search_items,
    }

    for title, details in titles_and_details.items():

        keywords = details.get('keywords', ())
        domains = details.get('domains', ())
        must_contain_all_keywords = details.get('must_contain_all_keywords', False)

        def filter_domains(search_item):
            """ to filter all the `search_item`s which are from `domains` """

            return domain_in_search(search_item, domains)

        def filter_keywords(search_item):
            """ to filter all the `search_item`s which contains `keyword` """
            return keyword_in_search(search_item, keywords, must_contain_all=must_contain_all_keywords)

        # filtering all results which contains `keyword`
        keywords_filtered = list(
            filter(
                filter_keywords,
                search_items
            )
        )

        # filtering all results which are from `domain`

        domains_filtered = list(
            filter(
                filter_domains,
                search_items
            )
        )

        search_data[title] = domains_filtered + keywords_filtered

    return search_data


def theme_filter(theme):
    """ filter the theme string, of something other than light or dark is provided, 
        then it returns light """

    return {
        "light": "light",

        "dark": "dark",
    }.get(theme, "light")


def get_current_theme(request):
    """ returns the value of current session variable 'theme' """
    
    return request.session.get("theme")


def get_requested_theme(request):
    """ 
        gets the currently requested theme, 
        by fetching the value of query parameter `theme` 
    """

    return request.GET.get("theme", None)


def set_new_theme(request, theme):
    """ sets the session variable `theme` to the desired value """

    theme = theme_filter(theme)
    request.session["theme"] = theme
    request.session.set_expiry(43800)


def get_theme_url(request, query, theme, start_index=None):
    """ returns the url to set a specific theme """

    # remove `q` parameter if it is not mentioned
    url_dict = {"q": query, "theme": theme} if query else {"theme": theme}

    # add `start` parameter to url
    if start_index:
        url_dict['start'] = start_index

    return request.path + "?" + urlencode(url_dict)
    

def perform_search(search_query, start_index=None):
    """ calls the CSE engine api to perform search and then classifies the results into appropriate categories"""

    API_KEY = config('API_KEY')
    CSE_KEY = config('CSE_KEY')

    has_prev_page = False
    has_next_page = False
    limit_reached = False

    prev_page_start_index = None
    next_page_start_index = None

    prev_page_url = None
    next_page_url = None

    result = {}

    if search_query:
        # calling api
        
        headers =  {
            'Accept-Encoding': 'gzip',
            'User-Agent': 'devXplore(gzip)',
        }
        start_query = f"start={start_index}" if start_index else ""
        custom_search_url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={CSE_KEY}&q={search_query}&fields=queries(previousPage,nextPage),items(title,link,snippet,htmlSnippet,htmlFormattedUrl)&{start_query}"

        response = requests.get(
            custom_search_url,
            headers=headers
        )
        result = response.json()

        if 'queries' in result.keys():
            queries = result['queries']

            has_prev_page = 'previousPage' in queries.keys()
            has_next_page = 'nextPage' in queries.keys()

            if has_prev_page:
                prev_page_start_index = queries['previousPage'][0]['startIndex']
                prev_page_url = search_url_with_start_index(search_query, prev_page_start_index)

            if has_next_page:
                next_page_start_index = queries['nextPage'][0]['startIndex']
                if next_page_start_index > 91:
                    has_next_page = False
                next_page_url = search_url_with_start_index(search_query, next_page_start_index)

        # if an array is not returned 
        # it means that an error has occured
        # check if a key named `error` exists or not
        # if yes then print error message

        if 'error' in result.keys():
            if result['error']['code'] == 429: # request limit reached
                result = {}
                limit_reached = True

    original_search_data = result
    search_items = original_search_data.get('items', [])

    # all the categories and the keywords of that categories

    results = classify_search(search_items, {
        'youtube': {
            'keywords': ("youtube.com", "youtube",),
            'domains': ('youtube.com',)
        },
        'courses': {
            'keywords': ("courses", "course",),
            'domains': ('udemy.com', "udacity.com", "coursera.com")
        },
        'tutorials': {
            'keywords': ("tutorials", "tutorial", "get started", ),
            'domains': ("tutorialspoint.com")
        },
        'docs': {
            'keywords': ("docs", "documentation", "official documentation"),
            'domains': ()
        },
        'github': {
            'keywords': ("git", "github", "github link"),
            'domains': ("github.com", )
        },
        'code play':{
            'keywords': ("code", "game"),
            'domains': ("flexboxfroggy.com", "codepip.com"),
            'must_contain_all_keywords': True
        },
    })

    return {
        'results': results,
        'limit_reached': limit_reached,
        
        'has_next_page': has_next_page,
        'has_prev_page': has_prev_page,

        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url,
    }
