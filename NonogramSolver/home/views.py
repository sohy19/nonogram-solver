from django.shortcuts import render
from django.contrib import messages
from DGA.new_nonogen import main
from DGA.nonogram import Rules
from collections import deque


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
    print(col, row)
    
    for i in range(1, row+1):
        idx = f"row-hint{i}"
        row_hints.append(list(map(int,request.POST.get(idx).split())))
    for i in range(1, col+1):
        idx = "col-hint" + str(i)
        col_hints.append(list(map(int,request.POST.get(idx).split())))
    

    # print(col_hints)
    # print(row_hints)
    rules=Rules(lines=row_hints, columns=col_hints)
    # print(rules)

    answer = deque(main(rules, row, col,row*col, nPopulation = 500))

    data=[]
    for c in range(col):
        temp=[]
        for r in range(row):
            temp.append(answer.popleft())
        data.append(temp)
    
    # print(data)
    if '' not in row_hints and '' not in col_hints:
        iterations = 254
        return render(request, 'result.html', {'row': row, 'col': col, 'row_hints': row_hints, 'col_hints': col_hints, 'num': iterations, 'answer': data})
    else:
        messages.info(request, '힌트를 채워주세요.')