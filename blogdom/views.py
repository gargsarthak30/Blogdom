from django.shortcuts import  HttpResponseRedirect


def Index(request):
    return HttpResponseRedirect('/blogs/')