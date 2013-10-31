from django.http import HttpResponse
import os

def home(request):
    return HttpResponse("Hello, {}!".format(os.environ.get('HELLO', 'World')))
