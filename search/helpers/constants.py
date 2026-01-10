"""Search category configuration for classifying search results.

This module defines SEARCH_CATEGORY_DATA, which contains the classification
rules for organizing search results into different tabs/categories.

Each category can use multiple signals for classification:
    - domains: List of domains that belong to this category
    - domain_priority: If True, domain match alone is sufficient (score: 100)
    - keywords: Keywords to search for in link, title, and snippet
    - url_patterns: Patterns to match in the URL path
    - title_patterns: Patterns to match in the page title
    - must_contain_all_keywords: If True, all keywords must be present
    - exclude_if_matched: Don't include if already matched these categories

The scoring system awards points for different matches:
    - Domain match with priority: 100 points (instant match)
    - Domain match: 50 points
    - URL pattern match: 30 points
    - Title pattern match: 25 points
    - Keyword match: 20 points

Items need a minimum score of 20 to be included in a category.
"""

# Description: Constants to categorize search results
SEARCH_CATEGORY_DATA = {
    "youtube": {
        "domains": ("youtube.com", "youtu.be"),
        "domain_priority": True,  # Domain match is sufficient
    },
    "stack overflow": {
        "domains": ("stackoverflow.com", "stackexchange.com"),
        "domain_priority": True,
    },
    "courses": {
        "keywords": ("course", "tutorial", "learn", "training", "bootcamp"),
        "domains": ("udemy.com", "udacity.com", "coursera.org", "pluralsight.com",
                    "educative.io", "codecademy.com", "freecodecamp.org"),
        "url_patterns": ("/course/", "/courses/", "/learn/"),
    },
    "documentation": {
        "keywords": ("documentation", "docs", "api reference", "guide"),
        "domains": ("readthedocs.io", "docs.python.org", "developer.mozilla.org"),
        "url_patterns": ("/docs/", "/documentation/", "/reference/"),
        "title_patterns": ("documentation", "docs", "api"),
    },
    "github": {
        "domains": ("github.com", "gitlab.com", "bitbucket.org"),
        "domain_priority": True,
    },
    "interactive": {
        "keywords": ("playground", "interactive", "practice", "game", "challenge"),
        "domains": ("codepen.io", "jsfiddle.net", "repl.it", "codesandbox.io",
                    "flexboxfroggy.com", "codepip.com"),
        "title_patterns": ("playground", "interactive", "try online"),
    },
    "blog articles": {
        "keywords": ("blog", "article", "guide", "how to", "explained"),
        "url_patterns": ("/blog/", "/article/", "/post/"),
        # Exclude if already matched by other categories
        "exclude_if_matched": ["documentation", "courses"],
    },
}
