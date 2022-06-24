from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect

# Create your views here.
from member.models import Member

# 회원가입 처리 함수
def join(request):
    returnPage = 'member/join.html'

    if request.method == 'GET':
        return render(request, returnPage)

    elif request.method == 'POST':
        form = request.POST.dict()
        # print(form, form['userid'])  # 전송된 데이터 확인

        # 유효성 검사 1/2, 3/4/5
        error = ''  # 검사 결과 저장용 변수
        if not (form['userid'] and form['passwd'] and form['repwd'] and form['name'] and form['email']):
            error = '회원 정보 값이 누락되었습니다'
        elif form['passwd'] != form['repwd']:
            error = '비밀번호가 일치하지 않습니다'
        else:
            # 입력한 정보를 Member 객체에 담음
            member = Member(
                userid=form['userid'], passwd=make_password(form['passwd']),  # 비밀번호는 암호화
                name=form['name'], email=form['email']
            )
            # Member 객체에 담은 회원정보를 member 테이블에 저장
            member.save()

            # 회원가입 성공시 joinok.html를 띄움
            returnPage = 'member/joinok.html'

        # 유효성 검사를 실패하는 경우
        # 오류내용을 join.html에 표시하기위해 dict 변수에 저장
        # 또한, 이미 입력했던 회원정보를 다시 join.html에 표시하기 위해
        # form이라는 dict 변수 생성
        context = {'form': form, 'error': error}

        return render(request, returnPage, context)

# 로그인 처리 함수
def login(request):
    returnPage = 'member/login.html'

    if request.method == 'GET':
        return render(request, returnPage)

    elif request.method == 'POST':
        form = request.POST.dict()

        # 유효성 검사 1/2
        error = ''
        if not (form['userid'] and form['passwd']):
            error = '아이디나 비밀번호가 입력되지 않았습니다'
        else:
            # 입력한 아이디로 회원정보가 테이블에 있는지 여부 확인
            try:
                member = Member.objects.get(userid=form['userid'])
            except Member.DoesNotExist:
                member = None

            if member and check_password(form['passwd'], member.passwd):
                # 아이디와 비밀번호 인증을 정상적으로 마쳤다면
                # 세션 변수에 인증정보를 저장해 둠
                request.session['userid'] = form['userid']

                # 로그인한 사용자의 id도 조회해서 세션변수에 저장해 둠
                id = Member.objects.all().filter(userid=form['userid']).values_list('id')[0][0]
                request.session['userid_id'] = id

                return redirect('/')  # index 페이지로 이동

            else:
                error = '아이디나 비밀번호가 틀립니다!'

        context = {'error': error}

        return render(request, returnPage, context)

# 로그인 회원의 정보 출력 함수
def myinfo(request):
    member = {}

       # 로그인한 회원 아이디를 알아냄 - 세션변수
    if request.session.get('userid'):
        userid = request.session.get('userid')

    # 아이디를 이용해서 member테이블에서 회원 정보를 알아냄
        member = Member.objects.get(userid=userid)

    context = {'member': member}
    return render(request, 'member/myinfo.html', context)

# 로그아웃 처리함수
def logout(request):
    # 만약 세션변수가 userid가 존재한다면 세션변수 삭제
    if request.session.get('userid'):
        del(request.session['userid'])

    # 로그아웃 후 index로 이동
        return redirect('/')

