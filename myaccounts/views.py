from django.contrib.auth.forms import UserChangeForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as origin_auth_login
from django.contrib.auth import logout as origin_auth_logout
from django.contrib.auth import get_user_model, authenticate
# from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from .forms import SignupForm, LoginForm
from django.urls import reverse
from django.contrib.auth.hashers import check_password

from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserSerializer, SearchUserSerializer
from django.views.decorators.csrf import csrf_exempt
from maps.models import Stamp

# 회원가입
# db저장ok / 비밀번호 유효검사 안됨ㅠㅠ
@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.user.is_authenticated:
        return redirect('maps:main')
    if request.method == 'POST':
        # print("post로 넘어옴")
        user_form = SignupForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            print("유효해")
            user.nickname = request.POST.get('username')
            user = user.save()
            # 저장한 user 정보 가져오기
            user_now = get_object_or_404(get_user_model(), email=request.POST.get('email'))
            # 자동 로그인
            origin_auth_login(request, user_now, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('maps:main')
        else:
            print("안 유효해")
            return render(request, 'maps/MainPage.html')
    return render(request, 'myaccounts/signUp.html')


# 로그인
@require_http_methods(['GET', 'POST'])
def login(request):
    print('로그인 들어옴')
    if request.user.is_authenticated:
        return redirect('maps:main')
    
    if request.method == 'POST':
        temp_email = request.POST.get('email')
        temp_password = request.POST.get('password')

        temp_user = get_object_or_404(get_user_model(), email=request.POST.get('email'))
        user = authenticate(request, username=temp_user.username, email=temp_email, password=temp_password)

        if user is not None :
            origin_auth_login(request, user)
            return redirect(request.GET.get('next') or 'maps:main')
        else:
            return render(request, 'maps/MainPage.html')
    else:
        form = LoginForm()
    context = {'login_form' : form, }
    return render(request, 'myaccounts/signIn.html', context)

# 로그아웃
@login_required
def logout(request):
    origin_auth_logout(request)
    return redirect('maps:main')

# 마이페이지
@login_required
@csrf_exempt
def mypage(request):
    bookmarks = request.user.bookmark_set.all()
    user = request.user
    dbuser = get_object_or_404(get_user_model(), email=user.email)
    stamps = Stamp.objects.filter(user=request.user)
    print('stamps', stamps)
    context = {"bookmark": bookmarks, 'dbuser': dbuser, 'stamps': stamps}
    print('db', dbuser)
    if request.method == "POST":
        print("post로 보냄")
        current_password = request.POST.get("origin_password")
        if request.POST.get('password1') == None :
            print("회원정보 수정이야")
            if check_password(current_password, user.password):
                dbuser.gender = request.POST.get('gender')
                dbuser.birth = request.POST.get('birth')
                dbuser.save()
                context['dbuser'] = dbuser
                return render(request, 'myaccounts/MyPage.html', context)
            else:
                print("비밀번호 오류")
                error_msg = "현재 비밀번호가 일치하지 않습니다."
                context['error_msg'] = error_msg
                return render(request, 'myaccounts/MyPage.html', context)
        else :
            print("비밀번호 변경이야")
            if check_password(current_password,user.password):
                new_password = request.POST.get("password1")
                password_confirm = request.POST.get("password2")
                if new_password == password_confirm:
                    user.set_password(new_password)
                    user.save()
                    user = authenticate(request, username=user.username, email=user.email, password=new_password)
                    if user is not None :
                        origin_auth_login(request, user)
                        return redirect(request.GET.get('next') or 'myaccounts:mypage')
                    return redirect("maps:main")
                else:
                    error_msg = "비밀번호가 일치하지 않습니다."
                    context['error_msg'] = error_msg
                    return render(request, 'myaccounts/MyPage.html', context)
            else:
                error_msg = "현재 비밀번호가 일치하지 않습니다."
                context['error_msg'] = error_msg
                return render(request, 'myaccounts/MyPage.html', context)
    return render(request, 'myaccounts/MyPage.html', context)

@api_view(['GET'])
def UserGetSerializer(request):
    '''
    모든 유저 정보
    '''
    users = get_user_model().objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET', 'DELETE'])
def UserInfoserializer(request, email):
    '''
    email로 유저 정보 가져오기
    email로 유저 정보 삭제
    '''
    user = get_object_or_404(get_user_model(), email=email)
    serializer = SearchUserSerializer(user, many=True)
    return Response(serializer.data)
