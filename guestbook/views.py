from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from guestbook.models import Guestbook


def guestbook(request):
    guestbook_list = Guestbook.objects.all().order_by('-regdate')
    print(guestbook_list)
    context = {'guestbook_list' : guestbook_list}

    return render(request, 'guestbook/list.html', context)

def add (request):
    guestbook = Guestbook()
    if request.POST['a'] == 'insert':
        guestbook.name = request.POST['name']
        guestbook.password = request.POST['pass']
        guestbook.message = request.POST['content']
        guestbook.save()

    return HttpResponseRedirect('/guestbook')

def deleteform(request):
    id = request.GET['id']
    id = {'id' : id}
    return render(request, 'guestbook/deleteform.html', id)

def delete(request):
    if request.POST['a'] == 'delete':
        id = request.POST['no']
        password = request.POST['password']
        Guestbook.objects.filter(id=id).filter(password=password).delete()

        return HttpResponseRedirect('/guestbook')