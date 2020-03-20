from django.template import Library


def get_item(dictionary, item):
    return dictionary.get(item)


register = Library()

register.filter('get_item', get_item)
