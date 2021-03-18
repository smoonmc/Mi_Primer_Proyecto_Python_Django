from django.db import models

# Create your models here.

"""Cada clase representa una tabla de la Base de datos
    y los campos son las columnas de la tabla.
"""

class Article(models.Model):
    title = models.CharField(max_length=150,verbose_name= "Título")
    content = models.TextField()
    image = models.ImageField(default='', upload_to="articles")
    public = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True) #el auto_now_add guarda la fecha cada registro insertado 
    updated_at = models.DateTimeField(auto_now=True) #auto_now guarda la fecha de actualización la ultima fecha

    class Meta:
        verbose_name = "Artículo"
        verbose_name_plural ="Artículos"
        ordering = ['id'] #para ordenar de menor a mayor
        #ordering = ['-id'] #para ordenar de mayor a menor

    def __str__(self): #ha esto le indican metodos mágicos de python buscar ejemplos en la web

        if self.public:
            public = "(publicado)"
        else:
            public = "(privado)"

        return f"{self.title} {public} "


class Category(models.Model):
    name = models.CharField(max_length=110)
    description = models.CharField(max_length=250)
    created_at = models.DateField()

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural ="Categorías"
