# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from practica.forms import FormularioRegistro, FormularioLogin
from lxml import etree
import requests
from pymongo import MongoClient


def inicio(request):
    return render(request, 'inicio.html')


def login(request):
    return HttpResponse("Login")


def bienvenida(request):
    return HttpResponse("Bienvenida")


def etsiit(request):
    # Descargar el árbol y extraer todos sus elementos address_component
    arbol_xml = etree.parse(
        'http://maps.googleapis.com/maps/api/geocode/xml?address=ETS+informatica+Granada&sensor=false')
    items = arbol_xml.xpath('//address_component')

    context = {}

    for i in items:
        # Sacar el tipo y el valor del elemento address_component
        tipo = i.xpath('./type')[0].text
        valor = i.xpath('./long_name')[0].text

        # En función del tipo meter el valor en un sitio del context.
        if tipo == 'administrative_area_level_1':
            context['provincia'] = valor
        elif tipo == 'locality':
            context['localidad'] = valor
        elif tipo == 'sublocality_level_1':
            context['distrito'] = valor

    return render(request, 'etsiit.html', context)


def buscador(request):
    etiqueta = ''
    noticias_insertadas = 0

    # Conexion con el cliente de Mongo
    cliente = MongoClient()
    # Seleccionar la base de datos
    baseDeDatos = cliente['noticias']
    # Seleccionar la coleccion dentro de la base de datos
    coleccion = baseDeDatos['noticias']

    if request.method == 'POST':
        borrar = request.POST['borrar']
        if borrar == 'false':
            # Sacar el xml utilizando requests
            # TODO hacer que se baje todas las paginas del pais, no solo la de portada
            r = requests.get('http://ep00.epimg.net/rss/elpais/portada.xml')
            # Cargar el xml en un etree
            arbolXML = etree.fromstring(r.content)
            # Las noticias son los items
            noticias = arbolXML.xpath('//item')
            noticias_parseadas = []

            for noticia in noticias:
                # Extraer titulo, fecha, etiquetas, descripcion y enlace de la noticia
                titulo = noticia.xpath('./title')[0].text
                fecha = noticia.xpath('./pubDate')[0].text

                # Buscar una noticia con el mismo titulo y la misma fecha
                busqueda_noticia = coleccion.find({'titulo': titulo, 'fecha': fecha})

                # Si no está repetida continúo.
                if busqueda_noticia.count() == 0:
                    descripcion = noticia.xpath('./description')[0].text
                    etiquetas = noticia.xpath('./category')
                    etiquetasParseadas = []
                    for e in etiquetas:
                        etiquetasParseadas.append(e.text)
                    enlace = noticia.xpath('./link')[0].text

                    #Meterlas en la coleccion
                    noticias_parseadas.append({"titulo": titulo,
                                               "descripcion": descripcion,
                                               "fecha": fecha,
                                               "etiquetas": etiquetasParseadas,
                                               "enlace": enlace
                                               })

            # Insertar las noticias en la base de datos si hay alguna que insertar
            noticias_insertadas = len(noticias_parseadas)
            if noticias_insertadas > 0:
                coleccion.insert_many(noticias_parseadas)
        elif borrar == 'true':
            # Borrar la coleccion entera
            coleccion.remove()

    else:
        etiqueta = request.GET.get('etiqueta', '')

    noticias = []

    if etiqueta != '':
        # Hacer la consulta
        elementos = coleccion.find({'etiquetas': etiqueta})
        print 'Buscando con etiqueta ' + etiqueta
    else:
        elementos = coleccion.find()
        print 'Buscando todos'
    # Parsear la consulta
    for resultado in elementos:
        noticias.append({"titulo": resultado['titulo'],
                         "descripcion": resultado['descripcion'],
                         "fecha": resultado['fecha'],
                         "enlace": resultado['enlace']
                         })
    # Meter las noticias en el contexto
    context = {'noticias': noticias, 'insertadas': noticias_insertadas}

    return render(request, 'buscador.html', context)


def imagenes(request):
    # Sacar el xml de las últimas noticias de El País
    arbolXML = etree.parse('http://ep00.epimg.net/rss/tags/ultimas_noticias.xml')
    # Coger una lista con todos los ítems de tipo enclosure, que son los que tienen imágenes.
    enclosures = arbolXML.xpath('//enclosure')

    imagenes = []

    for e in enclosures:
        # Coger el atributo url del enclosure
        url = e.get('url')
        # Coger una etiqueta de tipo link del padre del enclosure
        link = e.xpath('../link')[0].text
        # Añadir a la lista de imagenes un diccionario con la url y el link.
        imagenes.append({'url': url, 'link': link})

    context = {'imagenes': imagenes}

    return render(request, 'imagenes.html', context)


def registro(request):
    if request.method == 'POST':
        form = FormularioRegistro(request.POST)

        if form.is_valid():
            # Registrar el nuevo usuario
            nombre = form.cleaned_data['nombre']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            try:
                user = User.objects.create_user(nombre, email, password)
                user.save()

                context = {
                    'usuarioRegistrado': True,
                }
            except:
                context = {
                    'errores': True,
                    'error': "El usuario ya existe en la base de datos"
                }
                return render(request, 'registro.html', context)

            return render(request, 'inicio.html', context)
        else:
            context = {
                'form': form,
                'errores': True,
                'error': form.errors,
            }
            return render(request, 'registro.html', context)
    else:
        form = FormularioRegistro()

        context = {
            'form': form,
        }

        return render(request, 'registro.html', context)


def login(request):
    if request.method == 'POST':
        form = FormularioLogin(request.POST)

        if form.is_valid():
            # Intentar logear
            nombre = form.cleaned_data['nombre']
            password = form.cleaned_data['password']

            user = authenticate(username=nombre, password=password)

            # Ver si ha habido éxito
            if user is not None:
                if user.is_active:
                    # Mandar a bienvenida
                    context = {
                        'nombre': nombre,
                        'email': user.email,
                        'logged': True,
                    }
                    return render(request, 'bienvenida.html', context)
                else:
                    # El usuario no está activo
                    context = {
                        'errores': True,
                        'error': "El usuario está inactivo",
                    }
                    return render(request, 'login.html', context)
            else:
                # Error introduciendo usuario o contraseña
                context = {
                    'errores': True,
                    'error': "Usuario o contraseña son incorrectos",
                }
                return render(request, 'login.html', context)
        else:
            context = {
                'form': form,
                'errores': True,
                'error': form.errors,
            }

            return render(request, 'login.html', context)
    else:
        form = FormularioLogin()

        context = {
            'form': form,
        }

        return render(request, 'login.html', context)

