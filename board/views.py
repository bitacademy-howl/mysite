from django.shortcuts import render

# Create your views here.
def board(request):
    return render(request, 'board/list.html')

def modifyform(request):
    return render(request, 'board/modify.html')

def viewform(request):
    return render(request, 'board/view.html')

def writeform(request):
    return render(request, 'board/write.html')