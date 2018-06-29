from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'main/index.html')

def login(request):
    return render(request, 'user/loginform.html')

def join(request):
    return render(request, 'user/joinform.html')

def modify(request):
    pass

def logout(request):
    pass

def board(request):
    return render(request, 'board/list.html')
