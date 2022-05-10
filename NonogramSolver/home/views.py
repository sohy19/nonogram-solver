from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')

def result(request):
    row = request.GET['row']
    col = request.GET['col']
    return render(request, 'result.html', {'row': row, 'col': col})