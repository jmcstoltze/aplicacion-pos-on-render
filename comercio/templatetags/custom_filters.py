from django import template

register = template.Library()

@register.filter
def punto_miles(valor):
    try:
        valor =int(valor)
        return f"{valor:,}".replace(",", ".".replace(" ", ".").replace(" ", "."))
    except (ValueError, TypeError):
        return 0   