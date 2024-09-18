from django import template

register = template.Library()


@register.filter
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})


@register.filter
def is_radio_select(widget):
    return widget.__class__.__name__ == 'RadioSelect'
