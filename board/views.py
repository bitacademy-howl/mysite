from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from board.models import Board
from user.models import User


def board(request):

    posts_list = Board.objects.all().order_by('-regdate')
    posts_list = {'posts_list': posts_list}
    return render(request, 'board/list.html', posts_list)


def modifyform(request):
    return render(request, 'board/modify.html')

def delete(request):
    id = request.GET['id']
    # 1. post의 id 를 추출
    # 2. 해당 포스트의 user를 현재 session 객체에 저장된 유저와 비교

    authuser_exist = request.session.get('authuser')
    if authuser_exist is not None:
        current_posts = Board.objects.filter(id = id)
        if current_posts.user.email == authuser_exist['email']:
            current_posts.delete()

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
    # try:
    #     if request.session['authuser'] is None:
    #         return HttpResponseRedirect('/user/loginform')
    #     else:
    #         return render(request, 'board/write.html')
    # except KeyError as kE:
    #     return HttpResponseRedirect('/user/loginform')

    return render(request, 'board/write.html')

def write(request):
    board = Board()
    board.title = request.POST['title']
    board.content = request.POST['content']


    # 아래부분은 수정해야 할 사항으로############################################################################################################
    # 현재는 이메일과 패스워드로 비교하여 쿼리셋의 첫번째 user를 선택하도록 정하고 테스트 하였지만.
    # 실제로는 email을 primary 키로, 혹은 같은 이메일은 등록이 불가하도록 정의하는 로직이 필요하며,
    # 이는 user 객체의 VO 를 재정의 하던지, 유저 등록 시 action 을 재정의 하던지 하여 해결하도록 할 것!
    board.user = (User.objects.filter(email = request.session.get('authuser')['email']).filter(password = request.session.get('authuser')['password']))[0]
    #############################################################################################################################################

    board.save()

    return HttpResponseRedirect('/board')

def view(request):
    # 게시판에서 id는 primary key, 즉 unique 하므로 장고 쿼리셋의 get 메서드를 사용하여 얻어오도록하자.
    # 자세한 내용 https://docs.djangoproject.com/en/2.0/topics/db/queries/ 참고
    posts_obj = Board.objects.get(id=request.GET['id'])
    print(posts_obj, type(posts_obj))
    posts_dict = {'posts': posts_obj}
    return render(request, 'board/view.html', posts_dict)

