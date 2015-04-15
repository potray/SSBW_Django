# -*- coding: utf-8 -*-
from django.shortcuts import render
from django import forms
from django.core.validators import validate_slug, RegexValidator

class FormularioRegistro (forms.Form):

	#Declaro cada uno de los componentes del formulario
	nombre = forms.CharField(
		label = "Nombre",
		required = True,		
		)
	email = forms.EmailField(
		label = "Correo",
		)
	password = forms.CharField(
		label = "Contraseña",
		required = True,
		)

class FormularioLogin (forms.Form):
	nombre = forms.CharField(
		label = "Nombre",
		required = True,
		)
	password = forms.CharField(
		label = "Contraseña",
		required = True,
		)


