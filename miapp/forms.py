from django import forms
from django.core import validators # Sirve para validar datos

class FormArticle(forms.Form):
    title = forms.CharField(
        label = "Titulo",
        max_length=20,
        required=True,
        widget=forms.TextInput(  #cambiar algun atributo       
            attrs={
                'placeholder':"Ingresa el Título",
                'class':"titulo_form_article"
            }
        ),
        validators=[
            validators.MinLengthValidator(4,'El titulo es demasiado corto'),
            validators.RegexValidator('^[A-Za-z0-9ñ ]*$', 'El titulo esta mal formado', 'invalid_title')
        ]
    )
    
    content = forms.CharField(
        label = "Contenido",
        widget = forms.Textarea,
        validators=[
            validators.MaxLengthValidator(100,'Te has pasado, has puesto mucho texto')    
        ]     
    )

    content.widget.attrs.update({
        'placeholder':"Ingresa el Contenido",
        'class':"contenido_form_article"

    })

    public_options = [
        (1, 'Si'),
        (0, 'No')
    ]

    public = forms.TypedChoiceField(
        label = "¿Publicado?", 
        choices = public_options
    )

