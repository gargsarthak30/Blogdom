from django.shortcuts import  HttpResponseRedirect, render, HttpResponse


def Index(request):
    return HttpResponseRedirect('/blogs/')