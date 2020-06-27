# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 17:06:27 2020

@author: USER
"""

import cv2
import numpy as np
import scipy.io as io
import convert as cv
import tensorflow as tf
import datetime as d

def nothing(x):
    pass

def Filter(hsv_image, lowerbound, uppderbound):
    mask = cv2.inRange(hsv_image, lowerbound, uppderbound)
    return mask

def Cam(output):
    i=0
    clas = 0;
    """
    
    
    
    """
    A1,A2 = int(50*4),int(50*2)
    D1,D2 = int(50*4 +224),int(50*2+224)
    cam = cv2.VideoCapture(0)
    #
    lower_color = np.array([161, 155, 84], dtype=np.uint8)
    upper_color = np.array([179, 255, 255], dtype=np.uint8)
    #classes = tf.one_hot(indices = [0,1,2,3,4,5,6,7], depth = 8).eval(session=tf.compat.v1.Session())
    
    classes = np.zeros((8,8))
    classes[[0,1,2,3,4,5,6,7],np.arange(8)] = 1
    name = "BGR"
    name2 = "imsize"
    cv2.namedWindow(name)
    cv2.createTrackbar('Class', name, clas, 7, nothing)
    while(True):
        key = cv2.waitKey(1)
        ret,frame = cam.read()
        ret = cam.set(3,640)
        ret = cam.set(4,480)
        
        frame = cv2.flip(frame,1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        bw = Filter(hsv,lower_color,upper_color)
        bw2 = frame[A2:D2,A1:D1]
        
        cv2.rectangle(frame,(A1-10,A2-10),(D1+10,D2+10),(0,155,0),5)
        
        cv2.imshow(name,frame)
        cv2.imshow(name2, hsv)
        cv2.imshow("name3", bw)
        
        new_class = cv2.getTrackbarPos('Class', name)
        new_shape = str(  np.transpose(classes[:,new_class] )  )
        if key == ord('l'):
            j = d.datetime.now()
            cv2.imwrite("out/sample/output%r.png"%j,bw2)
            cv.xml(j,new_class,new_shape)
            i+=1
        if key == ord('q'):
            
            break
    
    cam.release()
    cv2.destroyAllWindows() 
    
    
    """save a binary image when press a key"""
    """save the image"""

def main():
    #infile = io.loadmat('training/polygons.mat')
   # gnd = io.loadmat('training/metadata.mat')
    #voc = io.loadmat('hand_dataset/test_dataset/test_data/annotations/VOC2007_1.mat')
    
   # x = infile['polygons'][0,4]
   # print(x)
    out = "out/output"
    Cam(out)
        
if __name__ == '__main__':
    main()
    

"""
    i=0
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output'+string(i)+'.avi',fourcc, 20.0, (640,480))
    i+=1
    
Use tensorflow
0. Get the camera working.
1. Find a way to annotate data
2. Compress image (conv2D already   ?)
3. Get dataset: 0,1,2,3,4,5,thumb up, half cross --> y = 8x1 
    7 envs: in (room), in (living-room), out-bright, out-buildings, out-tree, unlikely online place, unlikely online place
   
   4 possible views: front, back, 45d front,  45d back.
   20 for each
   
   9*6*30 = 1600.
4. Build a classic classification convnet 
5. Train it: with back propagation, epoch, compute stuff. Save checkpoint.



YOLOv3 hand
0. Get the camera working V

1. Implement first model

2. Get Dataset
2.1 Annotator
3. Parsing dataset
4. Train first test
5. Train official


Why YOLO?
1. Realtime speed (at least quasi-realtime)
2. Compatible with other annotation type
3. For studying purposes
4. Unlike OpenCV, it works everywhere on the screen esp in color.
Con: doesn't work well with human poses, which requires CPM (which is GPU consuming); slow on CPU (like in weeks)

problems with other datasets
1. pascalVOC: small hands, static
2. ego: static
3. egogesture: black and white, classification

problems with other repos:
1. general-purpose: most are made for pascalVOC and COCO
2. compatibility: various annotation formats, meaning that either there must be a converter, which won't be version-agnostic
3. learning: as a learner simply reading from other repos without in-depth understanding is well-nigh impossible. Should only apply on optimizing
4. deprecation: fuck it.

OpenCV and GoogLeNet?
Pros: fast, easy, implementable and compatible
Cons: from a camera only without a screen its hard to know where to put the hand. UNLESS there's a led signal telling to adjust the hand.
As part of the first undertaking, use OPENCV

Upgrade2: use YOLO-lite ( YOLOvWEB, less accurate, but doable on a laptop :((  )
Upgrade: use YOLOv3 to class hands (require massive dataset which is inhibiting)

"""
