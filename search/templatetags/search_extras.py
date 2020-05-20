from django.template import Library


def get_item(dictionary, item):
    return dictionary.get(item)


def to_hyphens(string):
    return string.lower().replace(" ", "-")


register = Library()
register.filter('get_item', get_item)
register.filter('to_hyphens', to_hyphens)
