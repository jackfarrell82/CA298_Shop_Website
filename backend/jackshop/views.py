from django.shortcuts import render

# Create your views here.

def index(request):
    # get the request in
    # do some logic with models from the databasse
    # return some webpage to the user
    dic = {'name':'Jack', 'Title':'Mr'}
    names = ['John', 'Paul', 'George', 'Ringo']
    return render(request, "index.html", {'names': names})