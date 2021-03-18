from django.shortcuts import render, HttpResponse, redirect
from miapp.models import Article, Category
from django.db.models import Q #esto espara hacer consultar con comando OR
from miapp.forms import FormArticle
from django.contrib import messages #esto sirve para mensajes flash/ sesiones flash


# Create your views here.
# MVC = Es el modelo vista Controlador -> Hay Acciones (metodos)
# MVT = Es el modelo Vista Template -> Acciones (metodos)

layout = """
<h1> Sitio web con Django | M. Cecilia Reyes </h1>
<hr/>
<ul>
   <li>
       <a href="/inicio" >INICIO</a>
   </li>
   <li>
       <a href="/hola-mundo" >HOLA MUNDO</a>
   </li>
   <li>
       <a href="/pagina" >PAGINA</a>
   </li>
    <li>
       <a href="/contacto" >CONTACTOS</a>
   </li>
</ul>
<hr/>
"""


def index(request):
    """ COMENTAMOS

    html = ""
       <h1> Inicio </h1>
       <p>Años hasta el 2050: </p>
       <h2> Son número pares: </h2> 
       <ul>    
    ""
    year = 2021
    while year <= 2050:
        if year % 2 == 0:
           html += f"<li>{str(year)} </li>"
        
        year +=1
    html +="</ul>"
    """ 
    year = 2021
    hasta = range(year, 2051)

    nombre = 'Cecilia'
    lenguajes = ['JavaScript', 'Python', 'PHP']

 
    return render(request, 'index.html', {
        'title': 'Inicio 2',
        'mi_variable':'Soy un dato que esta en la vista',
        'nombre': nombre,
        'lenguajes': lenguajes,
        'years': hasta
    })


def hola_mundo(request):
    return render(request, 'hola_mundo.html')

def pagina(request, redirigir=0):

    if redirigir == 1:
        return redirect("contacto", nombre="Cecilia", apellidos="Reyes")

    return render(request,'pagina.html',{'texto': 'Ejemplo 2' , 'lista':['uno','dos', 'tres']} )

def contacto(request):

    return render(request,'contacto.html')
    #return HttpResponse (layout+f"<h2>Contacto</h2>"+html)

#Esta definicion es para enviar los datos por la URL
def crear_articulo(request, title, content, public):

    articulo = Article(
        title = title,
        content = content,
        public = public
     
    )
    articulo.save() #con este comando guardo en la base de datos :)

    return HttpResponse(f"Articulo Creado: {articulo.title} - {articulo.content} ")

#con esta definición vamos a usar Formularios
def save_articulo(request):

    if request.method == "POST":

        title = request.POST['title']
        content = request.POST['content']
        public = request.POST['public']

        if len(title) <=1:
            return HttpResponse("<h2>El titulo es muy pequeño </h2>")


        articulo = Article(
            title = title,
            content = content,
            public = public
        )
        articulo.save()

        return HttpResponse(f"Articulo Creado: {articulo.title} - {articulo.content} ")

    else:
        return HttpResponse("<h2>No se ha podido crear el articulo </h2>")



def create_article(request):
   return render(request, 'create_article.html')

def create_full_article(request):

    if request.method == "POST":   
       formulario = FormArticle(request.POST)

       if formulario.is_valid():
          data_form = formulario.cleaned_data

          title = data_form.get('title')
          content = data_form['content']
          public = data_form['public']

          #Guardamos en la BD
          articulo = Article(
            title = title,
            content = content,
            public = public
          )
          articulo.save()

          #crear mensaje flash (sesion que solo se muestra 1 vez)
          messages.success(request, f"Has creado correctamente el articulo: {articulo.id}")
           
          return redirect('articulos') 
          #return HttpResponse(articulo.title + '-' + articulo.content + '-' + str(articulo.public))

    else:
        formulario = FormArticle()

    formulario = FormArticle()
    return render(request, 'create_full_article.html',{'form':formulario})


def articulo(request):
    try:
       sql = Article.objects.get(pk=4, public=True) #con esto estamo rescatando el registro id 4 de la BD.
       response = f"Articulo: <br/> {sql.content} - {sql.title} "
    except:
       response = "<h1>Artículo no encontrado</h1>"
    
    return HttpResponse(response)


def editar_articulo(request, id):
 
    sql =  Article.objects.get(pk=id)
    sql.title = "Tercer Articulo"
    sql.content = "Tercer contenido"
    sql.public = False

    sql.save()

    return HttpResponse(f"Articulo {sql.id} Editado: {sql.title} - {sql.content} ")


def articulos(request): 

    articulos = Article.objects.filter(public=True).order_by('-id') #Mostrar todos los articulos de la BD ordenado de manera descendente.
    #articulos = Article.objects.all.order_by('-id') #mostrar todos
    #articulos = Article.objects.order_by('title') [:3]
    #articulos = Article.objects.filter(id=6) #con esta opcion puedo filtra por campos
    #articulos = Article.objects.filter(title__exact = "articulo")  # Saca el titulo exacto
    #articulos = Article.objects.filter(title__iexact = "Articulo") #no distingue manyusculas ni minusculas
    #articulos = Article.objects.filter(id__gt=1) #Trae los registros mayores al ID 1
    #articulos = Article.objects.filter(id__gte=1)#Trae los registros mayores eh igual al ID 1
    #articulos = Article.objects.filter(id__lt=6)#Trae los registros menores al ID 6
    #articulos = Article.objects.filter(id__lte=6)#Trae los registros menores o iguales al ID 6
    #articulos = Article.objects.filter(id__lte=5, title__contains="Articulo")#Trae los registros menores o iguales al ID 65 y que contienen la parla Articulo en el titulo-
    #articulos = Article.objects.filter(title__contains= "Articulo").exclude(public=False)
    #articulos = Article.objects.filter(public=False)
    """
    #Esto es para hacer filtro con condición OR
    articulos = Article.objects.filter(
        Q(title__contains="Primer") | Q(title__contains="Cuarto")
    )
    """

    #TAMBIEN PODEMOS HACER CONSULTAS EN DURO; PERO NO ES RECOMENDABLE
    #articulos = Article.objects.raw("SELECT * FROM miapp_article WHERE title like '%Cuarto%'") 

    return render(request, 'articulos.html', {
        'articulos': articulos
    })


def borrar_articulo(request, id):
    articulo = Article.objects.get(pk=id)
    articulo.delete()

    return redirect('articulos')