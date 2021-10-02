from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
import cv2
import numpy as np
import mediapipe as mp
import json
from .models import RankingBoard
from .redis_client import RedisRanker
from .ML import sendResult,test

# Create your views here.
def index(request):
    '''처음 메인 화면'''
    return render(request, 'MG/index.html')

def us(request):
    return render(request, 'MG/about-us.html')

def cart(request):
    return render(request, 'MG/cart.html')

def checkout(request):
    return render(request, 'MG/check-out.html')

def contact(request):
    return render(request, 'MG/contact.html')

def error(request):
    return render(request, 'MG/error.html')

def features(request):
    return render(request, 'MG/features.html')

def login(request):
    return render(request, 'MG/login.html')

def profile(request):
    return render(request, 'MG/profile.html')

def registration(request):
    return render(request, 'MG/registration.html')

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
    '''ranking board 출력 화면 기능'''

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
        
        if rank_lists is None:
            return render(request, 'MG/ranking_board.html', {'data': None})

        for rank, name, score in rank_lists:
            item = dict({
                'ranking' : rank,
                'name' : name,
                'score' : score
            })
            rank20['rank' + str(rank)] = item
        # print(rank20)
        
        return render(request, 'MG/ranking_board.html', {'data': rank20})

# 기존 landmark와 Machinelearning으로 이동.


# <---------은수 코드 시작 --------->


### [문제1] Video는 화면전환 안되어있어서 q/w/e/r이 반대로 찍히는 문제 발생 -> r/e/w/q 로 순서를 걍 바꿔버림 (해결?임시방편?)
### [문제2] testMediaPipeHand 이동하면 JS Console에 에러가 찍히는 문제 -> 
### [문제3] 카메라에 손을 내리면 마지막에 저장된 location을 계속 출력하는 문제  -> ajax 통신후 좌표값을 전달하면 랜드마크를 저장하는 X를 NaN으로 초기화
### -> 전달된 landmark가 없으니까 마지막으로 저장된 location값을 찍는 것 같음 (추측)
def landmark_data(request):
    knn = test() # 일단 Model 저장하는 부분 안되는 것 같아서 test 함수로 진행
    try :
        if request.method == 'POST':
            # print("HERE>>>")
            landmark = request.POST.get('landmarks')
            landmark_to_json = json.loads(landmark)
            location= sendResult(landmark_to_json, knn)

        return JsonResponse({'location' : location})
    except Exception as e :
        print(e)
        return JsonResponse({'location' : 'None'})

#<-------은수 코드 끝 ----------->
