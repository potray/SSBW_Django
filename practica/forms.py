# -*- coding: utf-8 -*-
from django import forms


class FormularioRegistro(forms.Form):
    # Declaro cada uno de los componentes del formulario
    nombre = forms.CharField(
        label="Nombre",
        required=True,
    )
    email = forms.EmailField(
        label="Correo",
    )
    password = forms.CharField(
        label="Contraseña",
        required=True,
    )


class FormularioLogin(forms.Form):
    nombre = forms.CharField(
        label="Nombre",
        required=True,
    )
    password = forms.CharField(
        label="Contraseña",
        required=True,
    )


