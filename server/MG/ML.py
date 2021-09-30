import json
import numpy as np
import cv2
import os
import sys

def test():
    knn=None
    if os.path.isfile('C:/project3/MotionGame/server/TEMPLATES/KNNAlgorithm') :
        knn = cv2.ml_KNearest.load('C:/project3/MotionGame/server/TEMPLATES/KNNAlgorithm')
    else :
        file = np.genfromtxt('C:/project3/MotionGame/server/TEMPLATES/gesture_train.csv', delimiter=',')
        angle = file[:,:-1].astype(np.float32)
        label = file[:, -1].astype(np.float32)
        knn = cv2.ml.KNearest_create()
        knn.train(angle, cv2.ml.ROW_SAMPLE, label)
        knn.save('C:/project3/MotionGame/server/TEMPLATES/KNNAlgorithm')
        
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
    ret, results= knn.predict(data)
    print(1)
    idx = int(results[0][0])
    x=np.mean(xloc)
    y=np.mean(yloc)
    print(results[0][0])
    results=int(results[0][0])
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

