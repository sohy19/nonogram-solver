from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')

def next(request):
    row = request.GET['row']
    col = request.GET['col']
    return render(request, 'next.html', {'row': row, 'col': col})

def result(request, row, col):
    row_hints = []
    col_hints = []
    for i in range(1, row+1):
        idx = f"row-hint{i}"
        row_hints.append(request.POST.get(idx))
    for i in range(1, col+1):
        idx = "col-hint" + str(i)
        col_hints.append(request.POST.get(idx))
    print(row_hints)
    return render(request, 'result.html', {'row': row, 'col': col, 'row_hints': row_hints, 'col_hints': col_hints})