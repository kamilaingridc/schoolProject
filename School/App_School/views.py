from django.shortcuts import render


def abre_index(request):
    return render(request, 'Index.html')


def enviar_login(request):
    return render(request, 'login.html')
