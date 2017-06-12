from django.shortcuts import redirect

def index(request):
    context = {}
    return redirect('admin:index')
