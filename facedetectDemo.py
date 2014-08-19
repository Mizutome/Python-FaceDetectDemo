#!/usr/bin/env python

import numpy as np
import cv2
import cv2.cv as cv
from video import create_capture
from common import clock, draw_str

help_message = '''
USAGE: facedetect.py [--cascade <cascade_fn>] [--nested-cascade <cascade_fn>] [<video_source>]
'''

def detect(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30), flags = cv.CV_HAAR_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:,2:] += rects[:,:2]
    return rects

def draw_rects(img, rects, color):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

def draw_circle(img, rects, color):
    for x1, y1, x2, y2 in rects:
        center_x = (x1+x2)/2
        center_y = (y1+y2)/2
        cv2.circle(img, (center_x, center_y), 5, color, thickness = 3)
        return (center_x, center_y)
    return (-1, -1)
        
def draw_number_line(img):
    color = (123, 123, 0)
    thick = 2
    fontScale = 1.5

    x_L0 =200
    x_L1 =300
    x_L2 =400
    x_L3 =500
    x_L4 =600
    y_L0 =100
    y_L1 =200
    y_L2 =300
    y_L3 =400
    y_L4 =500
    
    x_T0 =250
    x_T1 =350
    x_T2 =450
    x_T3 =510
    y_T0 =150
    y_T1 =250
    y_T2 =350

    cv2.line(img, (x_L0, y_L0), (x_L0, y_L3), color, thickness=thick)
    cv2.line(img, (x_L1, y_L0), (x_L1, y_L3), color, thickness=thick)    
    cv2.line(img, (x_L2, y_L0), (x_L2, y_L3), color, thickness=thick)
    cv2.line(img, (x_L3, y_L0), (x_L3, y_L3), color, thickness=thick)
    cv2.line(img, (x_L4, y_L0), (x_L4, y_L3), color, thickness=thick)
    
    cv2.line(img, (x_L0, y_L0), (x_L4, y_L0), color, thickness=thick)
    cv2.line(img, (x_L0, y_L1), (x_L3, y_L1), color, thickness=thick)
    cv2.line(img, (x_L0, y_L2), (x_L3, y_L2), color, thickness=thick)
    cv2.line(img, (x_L0, y_L3), (x_L4, y_L3), color, thickness=thick)
    
    cv2.putText(img, "1", (x_T0, y_T0), cv2.FONT_HERSHEY_SIMPLEX, fontScale, color, thick)
    cv2.putText(img, "2", (x_T1, y_T0), cv2.FONT_HERSHEY_SIMPLEX, fontScale, color, thick)
    cv2.putText(img, "3", (x_T2, y_T0), cv2.FONT_HERSHEY_SIMPLEX, fontScale, color, thick)
    cv2.putText(img, "4", (x_T0, y_T1), cv2.FONT_HERSHEY_SIMPLEX, fontScale, color, thick)
    cv2.putText(img, "5", (x_T1, y_T1), cv2.FONT_HERSHEY_SIMPLEX, fontScale, color, thick)
    cv2.putText(img, "6", (x_T2, y_T1), cv2.FONT_HERSHEY_SIMPLEX, fontScale, color, thick)
    cv2.putText(img, "7", (x_T0, y_T2), cv2.FONT_HERSHEY_SIMPLEX, fontScale, color, thick)
    cv2.putText(img, "8", (x_T1, y_T2), cv2.FONT_HERSHEY_SIMPLEX, fontScale, color, thick)
    cv2.putText(img, "9", (x_T2, y_T2), cv2.FONT_HERSHEY_SIMPLEX, fontScale, color, thick)
    cv2.putText(img, "clear", (x_T3, y_T1), cv2.FONT_HERSHEY_SIMPLEX, 1, color, thick)    

def position_number(x, y):
    x_L0 =200
    x_L1 =300
    x_L2 =400
    x_L3 =500
    x_L4 =600
    y_L0 =100
    y_L1 =200
    y_L2 =300
    y_L3 =400
    y_L4 =500
    
    if   x >= x_L0 and x <x_L1 and y >= y_L0 and y < y_L1:
        return 1
    elif x >= x_L1 and x <x_L2 and y >= y_L0 and y < y_L1:
        return 2
    elif x >= x_L2 and x <x_L3 and y >= y_L0 and y < y_L1:
        return 3
    elif x >= x_L0 and x <x_L1 and y >= y_L1 and y < y_L2:
        return 4
    elif x >= x_L1 and x <x_L2 and y >= y_L1 and y < y_L2:
        return 5
    elif x >= x_L2 and x <x_L3 and y >= y_L1 and y < y_L2:
        return 6
    elif x >= x_L0 and x <x_L1 and y >= y_L2 and y < y_L3:
        return 7
    elif x >= x_L1 and x <x_L2 and y >= y_L2 and y < y_L3:
        return 8
    elif x >= x_L2 and x <x_L3 and y >= y_L2 and y < y_L3:
        return 9
    elif x >= x_L3 and x <x_L4 and y >= y_L0 and y < y_L3:
        # clear password = 2
        return -2
    else:
        return -1
    
def draw_text(img, num):
    '''
    cv2.putText(img, text, org, fontFace, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]])
    '''
    color = (200,200,199)
    org = (0, 0)
    if num > 0 and num < 10:
        text = "Number is " + str(num)
    else:
        text = "No detect"
    cv2.putText(img, text, (10, 470), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 3)
            
def draw_text_password(img, num, password_text):
    '''
    cv2.putText(img, text, org, fontFace, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]])
    '''
    color = (200,200,199)
    org = (0, 0)
    if num > 0 and num < 10:
        password_text += str(num)
    else:
        pass
    #cv2.putText(img, password_text, (10, 470), cv2.FONT_HERSHEY_SIMPLEX, 1, (200,200,199), 3)
    return password_text
    
if __name__ == '__main__':
    import sys, getopt
    print help_message

    args, video_src = getopt.getopt(sys.argv[1:], '', ['cascade=', 'nested-cascade='])
    try: video_src = video_src[0]
    except: video_src = 0
    args = dict(args)
    cascade_fn = args.get('--cascade', "C:/opencv/data/haarcascades/haarcascade_frontalface_alt.xml")
    nested_fn  = args.get('--nested-cascade', "C:/opencv/data/haarcascades/haarcascade_eye.xml")

    cascade = cv2.CascadeClassifier(cascade_fn)
    nested = cv2.CascadeClassifier(nested_fn)

    cam = create_capture(video_src, fallback='synth:bg=C:/opencv/samples/cpp/lena.jpg:noise=0.05')

    timeCounter = 0
    positon_num_temp = 0
    DETECT_LOAD_TIME = 5
    password_text = "password = "
    while True:
        ret, img = cam.read()
        flipImg = cv2.flip(img, 1)
        #width, height = flipImg.shape[:2]
        #print width, height, "+++++++"
        # height = 480 , width = 640 #
        
        #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #gray = cv2.equalizeHist(gray)
        
        gray = cv2.cvtColor(flipImg, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        #cv2.imshow('temp', gray)
        t = clock()
        rects = detect(gray, cascade)
        print rects, " "
        
        #vis = img.copy()
        vis = flipImg.copy()

        draw_number_line(vis)
        #draw_rects(vis, rects, (0, 255, 0))
        center_x, center_y = draw_circle(vis, rects, (0, 255, 0))
        position_num = position_number(center_x, center_y)
        #print "position_num=", position_num
        if positon_num_temp == position_num:
            timeCounter += 1
            #print "timeCOunter=", timeCounter
            if timeCounter == DETECT_LOAD_TIME:
                #draw_text(vis, position_num)
                password_text = draw_text_password(vis, position_num, password_text)
            if timeCounter == DETECT_LOAD_TIME and position_num == -2:
                password_text = "password = "
        elif positon_num_temp != position_num:
            timeCounter = 0
            positon_num_temp = position_num
        cv2.putText(vis, password_text, (10, 470), cv2.FONT_HERSHEY_SIMPLEX, 1, (200,200,199), 3)    
            
        #counter_to_draw_text(position_num)  

        '''
        # eyes detect
        for x1, y1, x2, y2 in rects:
            roi = gray[y1:y2, x1:x2]
            vis_roi = vis[y1:y2, x1:x2]
            #cv2.imshow('roi', vis_roi)
            subrects = detect(roi.copy(), nested)
            draw_rects(vis_roi, subrects, (255, 0, 0))
        '''
        dt = clock() - t

        draw_str(vis, (20, 20), 'time: %.1f ms' % (dt*1000))
        cv2.imshow('facedetect', vis)

        if 0xFF & cv2.waitKey(5) == 27:
            break
    cv2.destroyAllWindows()

