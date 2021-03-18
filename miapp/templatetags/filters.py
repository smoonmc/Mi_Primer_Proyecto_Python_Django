from django import template 

register = template.Library()

@register.filter(name='saludo')

def saludo(value):

    largo = ''
    if len(value) > 50:
        largo = "<p>Tu nombres es muy largo</p>"

    return f"<h1 style='background:green;color:white;'> Bienvenido/a, {value} </h1>" + largo


