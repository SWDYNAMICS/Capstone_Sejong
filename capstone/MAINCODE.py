import cv2 as cv
import numpy as np
import os
import time
import math
import serial
from math import degrees,pi,atan,cos
import pygame

TARGET = 'person'
TARGET_ID = 0
CONFIDENCE_THRESHOLD = 0.4   
NMS_THRESHOLD = 0.4
TANGENT = 1.6782
PIXEL_WIDTH = 1280
CAMERA_DIST = 26 #cm
FOCAL_LENGTH = PIXEL_WIDTH/TANGENT
COLORS = [(255,0,0),(255,0,255),(0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]
GREEN =(0,255,0)
BLACK =(0,0,0)

FONTS = cv.FONT_ITALIC
class_names = []


os.chdir('C:\py_temp\capstone')
with open('classes.txt', "r") as f:
    class_names = [cname.strip() for cname in f.readlines()]
#  setttng up opencv net
weight_path = 'yolov4-tiny.weights'
cfg_path = 'yolov4-tiny.cfg'

yoloNet = cv.dnn.readNet(weight_path, cfg_path)
yoloNet.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
yoloNet.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA_FP16)

model = cv.dnn_DetectionModel(yoloNet)                                  #dnn model 
model.setInputParams(size = (416,416),scale = 1/255, swapRB =True)
arduino = serial.Serial(port = 'COM10', baudrate = 9600, timeout=2)
time.sleep(3)
#setInputParams (double scale, Size size, Scalar mean, bool swapRB, bool crop)
def object_detector(image):
    classes, scores, boxes = model.detect(image,CONFIDENCE_THRESHOLD,NMS_THRESHOLD)
    data_list =[]
    idx = np.where(classes == [TARGET_ID])[0]
    cx = list(map(lambda i: boxes[i][0]+boxes[i][2]/2,idx))
    cx.sort()

    for (classid, score, box) in zip(classes, scores, boxes): #zip(classes=[[67],[1],[2]]  / scores = [0.7,0.8,0.5] / boxes=[[1,2,3,4,],[5,6,7,8],[9,1,2,3]]    )
        color = COLORS[int(classid) % len(COLORS)]
        label = "%s , %f" % (class_names[classid[0]], score)
        
        cv.rectangle(image, box, color, 2)
        cv.putText(image, label, (box[0],box[1]-14), FONTS, 0.5, color, 2)

        if classid == TARGET_ID:
            data_list.append([class_names[classid[0]], cx]) 
    return data_list    #data_list [name, cx=[cx1,cx2]]

def measure_one_distance(Ax,Bx):
    #-----mesuring distance...-----
    dist = (CAMERA_DIST*PIXEL_WIDTH)/(TANGENT*abs(Ax-Bx))
    #---------------------------
    return dist

def angle_mesurement(rx,lx):
    #-----mesuring angle...-----
    ratio_rx = (rx-PIXEL_WIDTH/2)/FOCAL_LENGTH
    ratio_lx = (lx-PIXEL_WIDTH/2)/FOCAL_LENGTH
    alpha = pi/2 - atan(ratio_rx)
    beta = pi/2 - atan(ratio_lx)
    angle = (alpha + beta)/2
    #---------------------------
    return angle

def write_read(x):
    x = x.encode('utf-8')
    arduino.write(x)
    # time.sleep(0.1)
    data = arduino.readline()
    return data


lcap = cv.VideoCapture(2, cv.CAP_DSHOW)
lcap.set(3,1280)
lcap.set(4,720)

rcap = cv.VideoCapture(0, cv.CAP_DSHOW)
rcap.set(3,1280)
rcap.set(4,720)

# video output frame by frame
iter = 1
pygame.init()
announcement = pygame.mixer.Sound('sample.wav') 
announcement.play(-1)
announcement.set_volume(0)
flag = True
while True:
    print('\n[   ',iter,"frame   ]")
    r_ret, r_frame = rcap.read() 
    l_ret, l_frame = lcap.read()
    if r_ret==False or l_ret==False:          
        print('We need to confirm whether both cameras work')          
        break 
    else:
        r_data = object_detector(r_frame)
        l_data = object_detector(l_frame)
        ddx = 0
        d=[]
        angle = []
        ang = '0'
        for rd,ld in zip(r_data,l_data):
            if rd[0] == TARGET and ld[0] == TARGET:
                crx = rd[1][ddx]
                clx = ld[1][ddx]
                d.append(measure_one_distance(crx,clx))
                angle.append(angle_mesurement(crx,clx))
                print('Object',ddx+1,'crx=',crx,'clx=',clx,'dist=',"{:.2f}".format(d[ddx]),'angle=',"{:.2f}".format(degrees(angle[ddx])))
                ddx = ddx + 1
        
        if len(d) >= 2:
            include_angle = angle[0] - angle[1]
            dist = math.sqrt(d[0]*d[0] + d[1]*d[1] - 2*d[0]*d[1]*cos(include_angle))
            print("distance between two person=","{:.2f}".format(dist))
            cv.putText(l_frame,"Distance:"+str(round(dist,3))+"Angle:"+str(degrees(round(include_angle,3))),(200,50),cv.FONT_HERSHEY_SIMPLEX, 1.2, (0,0,255),2)
            
            if dist < 120:
                flag = True
                ang = str(int(degrees(angle[1]*(5/6))))      
                value = write_read(ang)
                print('지목된사람의 각도:',ang)
                announcement.set_volume(1.0)
                print(value)
            elif dist > 120 and flag:
                flag = False
                announcement.set_volume(0.0)
                value = write_read('1')
                print(value)
        else:
            if flag:
                value = write_read('1')
                flag = False
                print(value)
                announcement.set_volume(0.0)
            
        

        cv.imshow('R_frame',r_frame)
        cv.imshow('L_frame',l_frame)
        iter = iter + 1
        
        key = cv.waitKey(1)        
        if key == ord('q'):
            value = write_read('0')
            print(value)
            break
lcap.release()
rcap.release()
cv.destroyAllWindows()