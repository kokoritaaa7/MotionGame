from django.http import HttpResponse
from .models import RankingBoard
from django.shortcuts import render

# Create your views here.
def us(request):
    return render(request, 'MG/about-us.html')

def cart(request):
    return render(request, 'MG/cart.html')

def check(request):
    return render(request, 'MG/check-out.html')

def tact(request):
    return render(request, 'MG/contact.html')

def err(request):
    return render(request, 'MG/error.html')

def fea(request):
    return render(request, 'MG/features.html')

def ind(request):
    return render(request, 'MG/index.html ')

def log(request):
    return render(request, 'MG/login.html')

def pro(request):
    return render(request, 'MG/profile.html')

def ragist(request):
    return render(request, 'MG/registratio.html')

def shopdetail(request):
    return render(request, 'MG/shop-details.html')

def shop(request):
    return render(request, 'MG/shop.html')

def tourna(request):
    return render(request, 'MG/tournaments-single.html')

def tour(request):
    return render(request, 'MG/tournaments.html')

def tour_sing(request):
    return render(request, 'MG/tour_sing.html')

def ranking_board(request):
    if request.method == 'GET':
        top20 = RankingBoard.objects.order_by('-score')[:20] # 상위 20개
        return render(request, 'testMotionGame/ranking_board.html', {'data': top20})
    else: # 검색 기능 필요
        id = request.POST.get('id')
        data = RankingBoard.objects.filter(name=id)

        ### 등수 어떻게 구하지? -> 물어보자
        # 다 가져오고 정렬해서 for문으로 idx 알아내서 같이 보내기
        # 랭킹매기는 함수(DB내에서)를 이용해서 구하고 조건을 통해서 받아오기
        # Redis 이용..? (django에서 redis 이용하려면 -> https://velog.io/@may_soouu/django-redis)
        # mysql에서 일정시간에 한번씩 랭킹을 계산하는 방법 -> 점수는 계속 점수테이블에 넣고, 서버에서 특정시간에 한번씩 랭킹 테이블에 계산한 값을 넣어주고, 클라에서는 랭킹테이블 값만 가져오면 됩니다. -> mysql 스케줄러 / 크론탭

        
        return render()


