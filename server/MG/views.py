from django.http import HttpResponse
from .models import RankingBoard
from .redis_client import RedisRanker
from django.shortcuts import render
import json

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

    import redis

    conn_redis = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
    gameRanker = RedisRanker(conn_redis, "game", False)
    

    if request.method == 'GET':
        top20_names = gameRanker.getTops()
        top20 = {}
        for idx, name in enumerate(top20_names):
            item = dict({
                'ranking':idx+1,
                'name': name,
                'score' : gameRanker.getScore(name)
            })
            top20['rank'+str(idx+1)] = (item)

        print(top20)

        return render(request, 'MG/ranking_board.html', {'data': top20})
    else: # 검색 기능 필요
        nickname = request.POST.get('nickname')

        ### REDIS로 처리하기
        # now_rank = gameRanker.getRank(nickname)
        rank_lists = gameRanker.findRank(nickname)
        # print(rank_lists)
        rank20 = {}
        
        for rank, name, score in rank_lists:
            item = dict({
                'ranking' : rank,
                'name' : name,
                'score' : score
            })
            rank20['rank' + str(rank)] = item
        # print(rank20)
        
        return render(request, 'MG/ranking_board.html', {'data': rank20})


