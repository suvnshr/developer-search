"""Search utility functions for categorizing and managing search results.

This module provides utilities for:
- Performing searches via SerpAPI
- Classifying search results into categories using a scoring system
- Managing pagination for search results
- URL and content pattern matching

The classification system uses multiple signals (domains, URL patterns, keywords,
title patterns) to intelligently categorize search results into tabs like
YouTube, Courses, Documentation, etc.
"""

import tldextract
from decouple import config
from rapidfuzz import fuzz
from serpapi import GoogleSearch

from . import constants


def search_url_with_page_index(query, page):
    """Returns URL for search results of next or previous page."""
    return f"?q={query}&page={page}"


def keyword_in_search(search_item, keywords=(), must_contain_all=False):
    """Checks if keywords are present in search item using exact and fuzzy matching.

    Args:
        search_item: Dict containing 'link', 'title', 'snippet' keys.
        keywords: Tuple of keywords to search for.
        must_contain_all: If True, all keywords must be present; otherwise any keyword.

    Returns:
        True if keywords match the criteria, False otherwise.
    """
    link = search_item.get("link", "")
    title = search_item.get("title", "")
    snippet = search_item.get("snippet", "")
    filter_func = all if must_contain_all else any

    for information in (link, title, snippet):
        if not information:
            continue

        # Exact substring match
        if filter_func(keyword.lower() in information.lower()
                       for keyword in keywords):
            return True

        # Fuzzy matching with 90% similarity threshold
        if filter_func(
            fuzz.WRatio(
                keyword,
                information,
                score_cutoff=90) for keyword in keywords):
            return True

    return False


def domain_in_search(search_item, domains=()):
    """Checks if search result is from any of the specified domains.

    Args:
        search_item: Dict containing 'link' key.
        domains: Tuple of domain strings to match against.

    Returns:
        True if result is from specified domains or if no domains specified.
    """
    link = search_item.get("link", "")

    if len(domains) == 0:
        return True

    for domain in domains:
        required_domain = tldextract.extract(domain).domain
        search_result_domain = tldextract.extract(link).domain

        if required_domain == search_result_domain:
            return True

    return False


def matches_pattern(text, patterns):
    """Checks if text contains any of the specified patterns.

    Args:
        text: String to search within.
        patterns: Tuple or list of pattern strings to match.

    Returns:
        True if any pattern is found in text (case-insensitive).
    """
    if not text:
        return False
    return any(pattern.lower() in text.lower() for pattern in patterns)


def score_search_item(search_item, category_config):
    """Scores a search item against category configuration.

    Uses multiple signals to calculate relevance:
    - Domain matching (50 points, or 100 for domain_priority categories)
    - URL patterns (30 points)
    - Title patterns (25 points)
    - Keyword matching (20 points)

    Args:
        search_item: Dict with 'link', 'title', 'snippet' keys.
        category_config: Dict with classification criteria.

    Returns:
        Integer score (0-100) indicating category match strength.
    """
    score = 0
    link = search_item.get("link", "")
    title = search_item.get("title", "")

    # Domain matching (highest priority)
    domains = category_config.get("domains", ())
    if domains and domain_in_search(search_item, domains):
        if category_config.get("domain_priority"):
            return 100
        score += 50

    # URL pattern matching
    url_patterns = category_config.get("url_patterns", ())
    if url_patterns and matches_pattern(link, url_patterns):
        score += 30

    # Title pattern matching
    title_patterns = category_config.get("title_patterns", ())
    if title_patterns and matches_pattern(title, title_patterns):
        score += 25

    # Keyword matching
    keywords = category_config.get("keywords", ())
    if keywords:
        must_contain_all = category_config.get(
            "must_contain_all_keywords", False)
        if keyword_in_search(search_item, keywords, must_contain_all):
            score += 20

    return score


def classify_search(search_items, category_configs):
    """Classifies search items into categories using scoring system.

    Each item is scored against each category and included if it meets
    the minimum threshold. Items can appear in multiple categories.

    Args:
        search_items: List of search result dicts.
        category_configs: Dict mapping category names to configuration dicts.

    Returns:
        Dict with 'all' key containing all items, plus keys for each category
        containing filtered items.
    """
    search_data = {"all": search_items}

    # Track which categories each item has been assigned to
    item_categories = {i: [] for i in range(len(search_items))}

    for category_name, config in category_configs.items():
        search_data[category_name] = []

        for idx, search_item in enumerate(search_items):
            score = score_search_item(search_item, config)

            # Minimum score threshold for inclusion
            if score >= 20:
                # Check exclusion rules
                exclude_if_matched = config.get("exclude_if_matched", [])
                if any(cat in item_categories[idx]
                       for cat in exclude_if_matched):
                    continue

                search_data[category_name].append(search_item)
                item_categories[idx].append(category_name)

    return search_data


def call_serpapi(search_query, page_index):
    """Calls SerpAPI to perform Google search.

    Args:
        search_query: Search query string.
        page_index: Starting index for pagination.

    Returns:
        Dict containing API response or error_code on failure.
    """
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
                api_response = {"error_code": 429}
            elif "Google hasn't returned any results for this query." in error_from_serpapi:
                api_response = {"error_code": 400}
            else:
                api_response = {"error_code": 500}

    except Exception as e:
        api_response = {"error_code": 500}

    return api_response


def perform_search_v2(search_query, page_index=0):
    """Performs search and classifies results into categories.

    Args:
        search_query: Query string to search for.
        page_index: Starting index for pagination (default: 0).

    Returns:
        Dict containing:
            - results: Classified search results by category
            - limit_reached: Whether API rate limit was hit
            - has_next_page: Whether more results are available
            - has_prev_page: Whether previous page exists
            - prev_page_url: URL for previous page
            - next_page_url: URL for next page
            - error_occured: Whether a server error occurred
    """
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
            pagination = api_response.get("pagination", {})
            has_prev_page = pagination.get("previous", False)
            has_next_page = pagination.get("next", False)

            if has_prev_page:
                prev_page_page_index = page_index - 1 if page_index > 0 else 1
                prev_page_url = search_url_with_page_index(
                    search_query, prev_page_page_index)

            if has_next_page:
                next_page_page_index = page_index + 1 if page_index > -1 else 1
                next_page_url = search_url_with_page_index(
                    search_query, next_page_page_index)

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
