from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
import cv2
import numpy as np
import mediapipe as mp
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

# 게임

def landmark_data(request):
    knn = test() # 일단 Model 저장하는 부분 안되는 것 같아서 test 함수로 진행
    if request.method == 'POST':
        # print("HERE>>>")
        landmark = request.POST.get('landmarks')
        landmark_to_json = json.loads(landmark)
        # print(landmark_to_json['landmarks'])
        location = sendResult(landmark_to_json, knn)

    return JsonResponse({'location' : location})

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