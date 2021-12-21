import cv2 as cv
import numpy as np

Lcap = cv.VideoCapture(0, cv.CAP_DSHOW)
Lcap.set(3,1280)
Lcap.set(4,720)

Rcap = cv.VideoCapture(2, cv.CAP_DSHOW)
Rcap.set(3,1280)
Rcap.set(4,720)

# video output frame by frame
iter = 1
while True:
    R_ret, R_frame = Rcap.read() 
    L_ret, L_frame = Lcap.read()
    if R_ret==False or L_ret==False:          
        print('We need to confirm whether both cameras work')          
        break 
    else:
        cv.imshow('R_frame',R_frame)
        cv.imshow('L_frame',L_frame)
        iter = iter + 1
        
        key = cv.waitKey(1)        
        if key == ord('q'):
            break
Lcap.release()
Rcap.release()
cv.destroyAllWindows()

