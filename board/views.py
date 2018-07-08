from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import DataError
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from board.models import Board
from user.models import User

def board(request):
    POST_IN_PAGES = 3
    RANGE_OF_PAGES = 5
    total_query_set = Board.objects.all().order_by('-regdate')

    paginator = Paginator(total_query_set, POST_IN_PAGES)
    pageNum = request.GET.get('pageNum')

    totalPageCount = paginator.num_pages

    try:
        posts_list = paginator.page(pageNum)
    # 초기 상태에 대한..
    except PageNotAnInteger:
        posts_list = paginator.page(1)
        pageNum = 1
    except EmptyPage:
        posts_list = paginator.page(paginator.num_pages)
        pageNum = paginator.num_pages

    pageNum = int(pageNum)

    start_index = 1+int((pageNum - 1) / RANGE_OF_PAGES) * RANGE_OF_PAGES
    end_index = start_index + RANGE_OF_PAGES-1
    if totalPageCount < end_index:
        end_index = totalPageCount

    bottomPages = range(start_index, end_index + 1)

    return render(request, 'board/list.html',
        {
            'posts_list': posts_list, 'pageNum': pageNum, 'bottomPages': bottomPages, 'totalPageCount': totalPageCount,
            'start_index': start_index, 'end_index': end_index
        })


def modifyform(request):
    id = request.GET['id']
    post = Board.objects.get(id=id)
    result = {'board_posts' : post}
    return render(request, 'board/modify.html', result)

def modify(request):
    id = request.POST['id']
    user = request.POST['user']
    title = request.POST['title']
    content = request.POST['content']

    posts = Board.objects.get(id=id)

    if request.session.get('authuser') is not None:
        if posts.user.email == request.session['authuser']['email']:
            try:
                posts.title = title
                posts.content = content
                posts.save()
                result = {'posts': posts}
                return render(request, 'board/view.html', result)
            except DataError:
                return render(request, 'board/modify.html', {'board_posts': posts, 'data_error' : True})
    else:
        return HttpResponseRedirect('/board')
    print(user)

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
    try:
        board = Board()
        board.title = request.POST['title']
        board.content = request.POST['content']
        # 아래부분은 수정해야 할 사항으로###############################################################################
        # 현재는 이메일과 패스워드로 비교하여 쿼리셋의 첫번째 user를 선택하도록 정하고 테스트 하였지만.
        # 실제로는 email을 primary 키로, 혹은 같은 이메일은 등록이 불가하도록 정의하는 로직이 필요하며,
        # 이는 user 객체의 VO 를 재정의 하던지, 유저 등록 시 action 을 재정의 하던지 하여 해결하도록 할 것!

        board.user = (User.objects.filter(email=request.session.get('authuser')['email']).filter(
            password=request.session.get('authuser')['password']))[0]
        ################################################################################################################
        board.save()
        return HttpResponseRedirect('/board')
    except DataError:
        return render(request, 'board/write.html', {'posts': board, 'data_error':True })

def view(request):
    # 게시판에서 id는 primary key, 즉 unique 하므로 장고 쿼리셋의 get 메서드를 사용하여 얻어오도록하자.
    # 자세한 내용 https://docs.djangoproject.com/en/2.0/topics/db/queries/ 참고
    posts_obj = Board.objects.get(id=request.GET['id'])
    posts_dict = {'posts': posts_obj}
    return render(request, 'board/view.html', posts_dict)

def delete(request):
    id = request.GET['id']
    posts = Board.objects.get(id=id)

    if request.session.get('authuser') is not None:
        if posts.user.email == request.session['authuser']['email']:
            Board.objects.filter(id=id).delete()

    return HttpResponseRedirect('/board')

