from django.shortcuts import render, redirect
from board.models import board
from member.models import Member

# Create your views here.

# 게시판 목록보기 처리


def list(request):
    bdlist = board.objects.values('id', 'title', 'userid', 'regdate', 'views')\
            .order_by('-id')

    context = {'bds': bdlist}
    return render(request, 'board/list.html', context)

#게시판 본문보기 처리
def view(request):
    return render(request, 'board/view.html')


# 게시판 글쓰기 처리
# get : board/write.html
# post : 작성한 글을 디비에 저장, 'board/index.html'
def write(request):
    returnPage = 'board/write.html'
    form = ''
    error = ''
    if request.method == 'GET':
        return render(request, returnPage)

    elif request.method == 'POST':
        form = request.POST.dict()

        # 유효성 검사 1/2
        if not (form['title'] and form['contents']):
            error = '제목이나 본문을 작성하세요!'
        else:
            # 입력한 게시글을 Board객체에 담음
            bd = board(title=form['title'], contents=form['contents'],
                       # 새글작성을 작성한 회원에 대한 정보는
                       # 회원테이블에 존재하는 회원번호(id)를 조회해서
                       # userid속성에 저장
                       userid=Member.objects.get(pk=form['memberid'])

                       )
            bd.save()  # board 객체에 담은 게시글을 테이블에 저장
            return redirect('/list')

    context = {'form':form, 'error':error}
    return render(request, returnPage, context)
