from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import RankingBoard
import cv2
import numpy as np
import mediapipe as mp
# import joblib
# import pyautogui
import json


# Create your views here.
def home(request):
    return render(request, 'testMotionGame/home.html')

# def studyImage(): 
#     file = np.genfromtxt('TEMPLATES/gesture_train.csv', delimiter=',')
#     angle = file[:,:-1].astype(np.float32)
#     label = file[:, -1].astype(np.float32)
#     knn = cv2.ml.KNearest_create()
#     knn.train(angle, cv2.ml.ROW_SAMPLE, label)
#     joblib.dump(knn, 'TEMPLATES/KNN_gestureModel.sav')

#     return knn


# def makeModeling():
#     try:
#         knn = joblib.load('TEMPLATES/KNN_gestureModel.sav')
#     except:
#         knn = studyImage()
#     # if knn is None:
#     #     knn = studyImage()
    
#     return knn

### [문제1] Video는 화면전환 안되어있어서 q/w/e/r이 반대로 찍히는 문제 발생 -> r/e/w/q 로 순서를 걍 바꿔버림 (해결?임시방편?)
### [문제2] testMediaPipeHand 이동하면 JS Console에 에러가 찍히는 문제
### [문제3] 카메라에 손을 내리면 마지막에 저장된 location을 계속 출력하는 문제 
#   -> 전달된 landmark가 없으니까 마지막으로 저장된 location값을 찍는 것 같음 (추측)
def landmark_data(request):
    knn = test() # 일단 Model 저장하는 부분 안되는 것 같아서 test 함수로 진행
    if request.method == 'POST':
        # print("HERE>>>")
        landmark = request.POST.get('landmarks')
        landmark_to_json = json.loads(landmark)
        # print(landmark_to_json['landmarks'])
        location = sendResult(landmark_to_json, knn)

    return JsonResponse({'location' : location})
''''''
def sendResult(landmarks, knn):
    # KNN 계산값 MediaPipe에 전달
    joint = np.zeros((21, 3))
    xloc, yloc  =[], []
    x, y = 0, 0
    location=''
        
    for j, lm in enumerate(landmarks['landmarks']):
        joint[j] = [lm['x'], lm['y'], lm['z']]
        xloc.append(lm['x'])
        yloc.append(lm['y'])
        x=np.mean(xloc)
        y=np.mean(yloc)

        # Compute angles between joints
        v1 = joint[[0,1,2,3,0,5,6,7,0,9,10,11,0,13,14,15,0,17,18,19],:] # Parent joint
        v2 = joint[[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],:] # Child joint
        v = v2 - v1 # [20,3]
        # Normalize v
        v = v / np.linalg.norm(v, axis=1)[:, np.newaxis]

        # Get angle using arcos of dot product
        angle = np.arccos(np.einsum('nt,nt->n',
            v[[0,1,2,4,5,6,8,9,10,12,13,14,16,17,18],:], 
            v[[1,2,3,5,6,7,9,10,11,13,14,15,17,18,19],:])) # [15,]""

        angle = np.degrees(angle) # Convert radian to degree

        # Inference gesture
        data = np.array([angle], dtype=np.float32)
        ret, results, neighbours, dist = knn.findNearest(data, 3)
        idx = int(results[0][0])
        if x<0.25 :
            location='r'
        if x<0.5 and x>0.25 :
            location='e'
        if x<0.75 and x>0.5 :
            location='w'
        if x>0.75 :
            location='q'
        
        # print(location)

    return location

def test():
    knn=None
    try :
        knn=cv2.ml.KNearest_load('KNNalgorithm')
        
    except :
        file = np.genfromtxt('TEMPLATES/gesture_train.csv', delimiter=',')
        angle = file[:,:-1].astype(np.float32)
        label = file[:, -1].astype(np.float32)
        knn = cv2.ml.KNearest_create()
        knn.train(angle, cv2.ml.ROW_SAMPLE, label)
        knn.save('KNNalgorithm')

    return knn

def ranking_board(request):
    if request.method == 'GET':
        top20 = RankingBoard.objects.order_by('-score')[:20] # 상위 20개
        return render(request, 'testMotionGame/ranking_board.html', {'data': top20})
    else: # 검색기능 필요
        id = request.POST.get('id')

    return render()
