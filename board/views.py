from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
def board(request):
    return render(request, 'board/list.html')

def modifyform(request):
    return render(request, 'board/modify.html')

def viewform(request):
    return render(request, 'board/view.html')

def writeform(request):

    # 인증 체크

    # 세션 객체의 겟 함수는 있을 경우 해당 키를, 없을경우 None을 반환해 주므로,
    # 예외가 발생하지 않는다.

    # 아래는 session.get() 에 대한 설명 : API 문서 참조
    # get(key, default=None)
    #       Example: fav_color = request.session.get('fav_color', 'red')

    authuser_exist = request.session.get('authuser')
    if authuser_exist is None:
        return HttpResponseRedirect('/user/loginform')

    # 아래의 코드는 로그인을 한번도 하지 않은 상태에서 상태에서 게시판을 누를때,
    # Keyerror를 발생시키므로, try exception 구문을 사용하여, 예외 처리를 하거나,
    # 혹은 위의 코드를 사용하도록 하자

    # print(request.session['authuser'], type(request.session['authuser']))
    #
    # if request.session['authuser'] is None:
    #     return HttpResponseRedirect('/user/loginform')

    return render(request, 'board/write.html')