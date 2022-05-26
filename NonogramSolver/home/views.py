from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')

def next(request):
    row = request.GET['row']
    col = request.GET['col']
    return render(request, 'next.html', {'row': row, 'col': col})

def result(request):
    return render(request, 'result.html')