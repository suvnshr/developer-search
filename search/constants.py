# Description: Constants to categorize search results
SEARCH_CATEGORY_DATA = {
        "youtube": {
            "keywords": (
                "youtube.com",
                "youtube",
            ),
            "domains": ("youtube.com",),
        },
        "courses": {
            "keywords": (
                "courses",
                "course",
            ),
            "domains": ("udemy.com", "udacity.com", "coursera.com"),
        },
        "tutorials": {
            "keywords": (
                "tutorials",
                "tutorial",
                "get started",
            ),
            "domains": ("tutorialspoint.com"),
        },
        "docs": {
            "keywords": ("docs", "documentation", "official documentation"),
            "domains": (),
        },
        "github": {
            "keywords": ("git", "github", "github link"),
            "domains": ("github.com",),
        },
        "code play": {
            "keywords": ("code", "game"),
            "domains": ("flexboxfroggy.com", "codepip.com"),
            "must_contain_all_keywords": True,
        },
    }
