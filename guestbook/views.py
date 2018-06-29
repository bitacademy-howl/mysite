from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from guestbook.models import Guestbook


def index(request):
    guestbook_list = Guestbook.objects.all().order_by('-regdate')

    context = {'guestbook_list' : guestbook_list}
    return render(request, 'guestbook/index.html', context)

def add (request):
    guestbook = Guestbook()
    guestbook.name = request.POST['name']
    guestbook.password = request.POST['password']
    guestbook.message = request.POST['message']

    guestbook.save()

    return HttpResponseRedirect('/guestbook')

def deleteform(request):
    id = request.GET['id']
    id = {'id' : id}
    return render(request, 'guestbook/deleteform.html', id)

def delete(request):
    id = request.POST['id']
    password = request.POST['password']
    # try:
    context = Guestbook.objects.filter(id=id).filter(password=password).delete()
    # except ValueError as vE:
    #     print('[Error name : {0}, Occured time : {1}'.format(vE, datetime.now()))

    return HttpResponseRedirect('/guestbook')