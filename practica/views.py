# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from practica2.forms import FormularioRegistro, FormularioLogin
from lxml import etree



def inicio (request):
	return render(request, 'inicio.html')

def login (request):
	return HttpResponse("Login")

def bienvenida (request):
	return HttpResponse("Bienvenida")

def etsiit (request):

	#Descargar el árbol y extraer todos sus elementos address_component
	arbolXML = etree.parse('http://maps.googleapis.com/maps/api/geocode/xml?address=ETS+informatica+Granada&sensor=false')
	items = arbolXML.xpath('//address_component')

	context = {}

	for i in items:
		#Sacar el tipo y el valor del elemento address_component
		tipo = i.xpath('./type')[0].text
		valor = i.xpath('./long_name')[0].text

		#En función del tipo meter el valor en un sitio del context.
		if tipo == 'administrative_area_level_1':
			context['provincia'] = valor
		elif tipo == 'locality':
			context['localidad'] = valor
		elif tipo == 'sublocality_level_1':
			context['distrito'] = valor

	return render (request, 'etsiit.html', context)

def imagenes (request):
	#Sacar el xml de las últimas noticias de El País
	arbolXML = etree.parse('http://ep00.epimg.net/rss/tags/ultimas_noticias.xml')
	#Coger una lista con todos los ítems de tipo enclosure, que son los que tienen imágenes.
	enclosures = arbolXML.xpath('//enclosure')

	imagenes = []

	for e in enclosures:
		#Coger el atributo url del enclosure
		url = e.get('url')
		#Coger una etiqueta de tipo link del padre del enclosure
		link = e.xpath('../link')[0].text
		#Añadir a la lista de imagenes un diccionario con la url y el link.
		imagenes.append({'url' : url, 'link' : link})

	context = {'imagenes' : imagenes}

	return render (request, 'imagenes.html', context)

def registro (request):
	if request.method == 'POST':
		form = FormularioRegistro (request.POST) 

		if form.is_valid ():
			#Registrar el nuevo usuario
			nombre = form.cleaned_data['nombre']
			password = form.cleaned_data['password']
			email = form.cleaned_data['email']
			try:
				user = User.objects.create_user(nombre, email, password)
				user.save()

				context = {
					'usuarioRegistrado' : True,
				}
			except:
				context = {
					'errores' : True,
					'error' : "El usuario ya existe en la base de datos"
				}
				return render(request, 'registro.html', context)

			

			return render(request, 'inicio.html', context)
		else:
			context = {
				'form' : form,
				'errores' : True,
				'error': form.errors,
			}
			return render(request, 'registro.html', context)
	else:
		form = FormularioRegistro()

		context = {
			'form': form,
		}

		return render(request, 'registro.html', context)

def login (request):
	if request.method == 'POST':
		form = FormularioLogin (request.POST)

		if form.is_valid ():
			#Intentar logear
			nombre = form.cleaned_data['nombre']
			password = form.cleaned_data['password']
			
			user = authenticate(username = nombre, password = password)

			#Ver si ha habido éxito
			if user is not None:
				if user.is_active:
					#Mandar a bienvenida
					context = {
						'nombre' : nombre,
						'email' : user.email,
						'logged' : True,
					}
					return render(request, 'bienvenida.html', context)
				else:
					#El usuario no está activo
					context = {
						'errores' : True,
						'error' : "El usuario está inactivo",
					}
					return render(request, 'login.html', context)
			else:
				#Error introduciendo usuario o contraseña
				context = {
					'errores' : True,
					'error' : "Usuario o contraseña son incorrectos",
		        }
				return render(request, 'login.html', context)
		else:
			context = {
				'form' : form,
				'errores' : True,
				'error': form.errors,
			}

			return render(request, 'login.html', context)
	else:
		form = FormularioLogin ()

		context = {
			'form' : form,
		}

		return render (request, 'login.html', context)