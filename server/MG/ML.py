import json
import numpy as np
import cv2
import os
import sys
from sklearn.neighbors import KNeighborsClassifier
from sklearn import datasets
import pickle
import pandas as pd
from joblib import dump,load
from django.conf import settings

## MachineLearing 부분 따로 떼어서 코드 작성.
def test():
    knn=None
    if os.path.isfile(os.path.join(settings.BASE_DIR, 'MG/static/KNNModel.joblib')) :
        knn = load(os.path.join(settings.BASE_DIR, 'MG/static/KNNModel.joblib'))
    else :
        DF=pd.read_csv(os.path.join(settings.BASE_DIR, 'MG/static/Gesturedata.csv'), header=None)
        X=DF[DF.columns[:15]]
        Y=DF[DF.columns[-1]]
        knn = KNeighborsClassifier(n_neighbors=1,metric='minkowski',p=2,weights='distance')
        knn.fit(X,Y)
        s=pickle.dumps(knn)
        dump(knn, os.path.join(settings.BASE_DIR, 'MG/static/KNNModel.joblib'))

                
    return knn

def sendResult(landmarks, knn):
    # KNN 계산값 MediaPipe에 전달
    joint = np.zeros((21, 3))
    xloc, yloc  =[], []
    x, y = 0, 0
    location='None'

    for j, lm in enumerate(landmarks['landmarks']):
        joint[j] = [lm['x'], lm['y'], lm['z']]
        xloc.append(lm['x'])
        yloc.append(lm['y'])

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
    results= knn.predict(data)
    idx = int(results)
    x=np.mean(xloc)
    y=np.mean(yloc)
    if results==1 or results==2 :
        if x<0.25 :
            location='r'
        if x<0.5 and x>0.25 :
            location='e'
        if x<0.75 and x>0.5 :
            location='w'
        if x>0.75 :
            location='q'

    return location

