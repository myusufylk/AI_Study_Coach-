from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Sözlükten anahtar değerine göre veri çeken template filtresi.
    Örn: {{ my_dict|get_item:key }}
    """
    if dictionary is None:
        return ""
    return dictionary.get(key, "")
