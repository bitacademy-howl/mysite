from django.db import DataError
from django.forms import model_to_dict
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from django.contrib import messages

# Create your views here.
from django.views import View

from user.models import User

def joinform(request):
    return render(request, 'user/joinform.html')

def joinsuccess(request):
    return render(request, 'user/joinsuccess.html')

def join(request):

    user = User()
    user.name = request.POST['name']
    user.email = request.POST['email']
    user.password = request.POST['password']
    user.gender = request.POST['gender']

    if User.objects.filter(email = user.email).exists() is not True:
        user.save()
        return HttpResponseRedirect('/user/joinsuccess')

    # 입력폼 비교 구문과 이에따른 메시지 생성을 별도의 함수내에 구현하고, 그 수행 결과에 따른 action 만을
    # 본 함수에서 구현하도록 한다.

    # 응답으로 되돌려줄 리턴 값은
    # email_available, user의 폼 입력 값들, 응답할 메시지
    # 세 가지로 한다.

    # elif len(User.objects.filter(email = user.email)) == 0:
    #     return render(request, 'user/joinform.html', {"email_availability": False, "user": user})
    else:
        return render(request, 'user/joinform.html', {"email_availability" : False, "user":user})

def loginform(request):
    return render(request, 'user/loginform.html')

def login(request):
    result = User.objects.filter(email=request.POST['email']).filter(password=request.POST['password'])
    # 로그인 실패
    if len(result) == 0:
        return HttpResponseRedirect('/user/loginform?result=false')

    # 로그인 처리
    authuser = result[0]
    request.session['authuser'] = model_to_dict(authuser)
    print(request.session['authuser'])

    # 텍스트를 그냥 출력해주는방법
    # return HttpResponse(authuser)
    return HttpResponseRedirect('/')

def logout(request):

    # 세션 초기화 : 아래와 다른점은 세션 종료 조건을 브라우저 종료 시 될 수 있도록, 장고 설정에 지정하였고,
    #               브라우저가 종료되지 않으면 사실상 해당 세션이 계속 남아 있게 된다.
    #               웹어플리케이션이 지금 단계에서 발전하여서 세션 객체에 더 많은 정보를 저장하게 된다면,
    #               모든 속성들을 다 초기화 해주어야 하는 점과, 로그아웃을 해도 세션이 유지된다는
    #               기이한 상황이 발생된다.
    #               해당 예제에서는 로그아웃 시 페이지 이동이 있고 http 요청을 다시 수행하므로,
    #               세션을 끊고 다시 리다이렉트 시 해당 연결에서 세션을 맺을 수 있도록 하는 것이 맞는 것 같다.

    # 아래는 참고.
    # flush() 함수 설명
    # Deletes the current session data from the session and deletes the session cookie.
    # This is used if you want to ensure that the previous session data can’t be accessed again
    # from the user’s browser(for example, the django.contrib.auth.logout() function calls it)

    request.session.flush()

    # 아니면 아래처럼 예외처리 : 현재 예제에서는 html 문서가 로그아웃될 경우 와 로그인 될 경우를
    # html 문서에서의 변경으로 처리하였지만, 사용자가 웹페이지 조작을 통해 예외를 일으킬 수 있는 코드이지만
    # 위의 코드는 웹페이지 조작으로 로그아웃 상태에서 로그아웃을 불러오더라도 예외가 발생하지 않는다.

    # try:
    #     del request.session['authuser']
    # except KeyError:
    #     pass

    return HttpResponseRedirect('/')
    
def modifyform(request):
    user = request.session.get('authuser')
    if user is None:
        return render(request, 'user/loginform.html')
    else:
        user_obj = User.objects.filter(email=user['email'])[0]
        return render(request, 'user/modifyform.html', {'user' : user_obj})

def modify(request):
    user = request.session.get('authuser')
    if user is not None:
        user_obj = User.objects.filter(email=user['email'])[0]
        user_obj.name = request.POST['name']
        user_obj.password = request.POST['password']
        user_obj.gender = request.POST['gender']
        try:
            user_obj.save()
            return HttpResponseRedirect('/')
        except DataError:
            return render(request, 'user/modifyform.html', {'user': user_obj, 'data_error': True})
    else:
        return render(request, 'user/loginform.html')