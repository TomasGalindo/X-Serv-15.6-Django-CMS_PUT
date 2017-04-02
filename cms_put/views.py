from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import urllib.request
# Create your views here.

from cms_put.models import Page


def notfound(request, rec):
    respuesta = "recurso " + rec + " no encontrado"
    return HttpResponse(respuesta)

def writeBase(request):
    respuesta = "Listado de las paginas que tienes guardadas. "
    lista_paginas = Page.objects.all()
    for pagina in lista_paginas:
        respuesta += "<br>" + pagina.name + " Id = " + str(pagina.id)
    respuesta += "<br>Debe buscar por Id"
    return HttpResponse(respuesta)


# BUSCANDO A TRAVES DEL IDENTIFICADOR
@csrf_exempt
def pagina(request, identificador):
    if request.method == "GET":
        # Buscar en la base de datos
        try:
            pagina = Page.objects.get(id=identificador)
            # si existe
            respuesta = "<a href=" + pagina.page + ">" + pagina.page + "</a>"
        except Page.DoesNotExist:
            # no existe
            respuesta = "No existe la pagina " + str(identificador)
            respuesta += "<form action='/pagina/8' method='post'>"
            respuesta += "Name: <input type= 'text' name='name'>"
            respuesta += "Page: <input type= 'text' name='page'>"
            respuesta += "<input type= 'submit' value='enviar'>"
            respuesta += "</form>"
    elif request.method == "POST":
        name = request.POST['name']
        page = request.POST['page']
        pagina = Page(name=name, page=page)
        pagina.save()
        respuesta = "HE HECHO UN POST, lo he guardado"
    elif request.method == "PUT":
        print("DETECTO PUT")
        prueba = request.body.decode('utf-8')
        name, page = prueba.split(",")
        pagina = Page(name=name, page=page)
        pagina.save()
        respuesta = "He detectado un PUT, Guardado"
    else:
        respuesta = "NO PUEDES HACER ESTA OPERACION"
    return HttpResponse(respuesta)
