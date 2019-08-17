# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 13:03:02 2019

@author: Kaushal
"""

import cv2
import numpy as np
#import matplotlib.pyplot as plt

def make_coordinates(image, lines_parameter):
    #print('lines parameter', lines_parameter)
    slope, intercept = lines_parameter
    y1 = image.shape[0]
    y2 = int(y1 *(3/5))
    x1 = int((y1-intercept)/ slope)
    x2 = int((y2-intercept)/ slope)
    return np.array([x1, y1, x2, y2])

def average_slope_interception(image, lines):
    left_fit = []
    right_fit = []
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1,x2), (y1,y2), 1)
        slope = parameters[0]
        intercept = parameters[1]
        if slope < 0:
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))
    left_fit_average = np.average(left_fit, axis = 0)
    right_fit_average = np.average(right_fit, axis = 0)

    try:
        left_line = make_coordinates(image, left_fit_average)
        right_line = make_coordinates(image, right_fit_average)
        return np.array([left_line, right_line])
    except Exception as e:
        print(e, '\n')
 #print error to console
        return None

#    left_line = make_coordinates(image, left_fit_average)
#    right_line = make_coordinates(image, right_fit_average)
    return np.array([left_line, right_line])

def canny(image):
    gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    canny = cv2.Canny(blur, 50, 150)
    return canny

def display_line(lines, image):
    line_image = np.zeros_like(image)
    if lines is not None:
        for x1, y1, x2, y2 in lines:
            cv2.line(line_image, (x1,y1), (x2,y2), (255,0,0), 10)
    return line_image

def region_of_intrest(image):
    height = image.shape[0]
    polygon = np.array([[(200, height),(1100, height),(550,250)]])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygon , 255)
    masked_image = cv2.bitwise_and(mask, image)
    return masked_image

#

#lane_image = np.copy(image)
#canny = canny(lane_image)
#canny = region_of_intrest(canny)
#lines = cv2.HoughLinesP(canny, 2, np.pi/180, 100, np.array([]),minLineLength = 40, maxLineGap = 5)
#average_line = average_slope_interception(lane_image, lines)
#line_image = display_line(average_line, canny)
#combo_image = cv2.addWeighted(lane_image, .8, line_image, 1,1)
##plt.imshow(region_of_intrest(combo_image))
#plt.imshow(combo_image)
#plt.show()
fps = 25
image = cv2.imread('test_image.jpg')
height, width, layers = image.shape
size = (width, height)
out = cv2.VideoWriter('video.avi', cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
cap = cv2.VideoCapture('test2.mp4')
frames = []
while (cap.isOpened()):
    ret , frame = cap.read()
    if ret:
        canny_image = canny(frame)
        canny_image = region_of_intrest(canny_image)
        lines = cv2.HoughLinesP(canny_image, 2, np.pi/180, 100, np.array([]), minLineLength = 40, maxLineGap = 5)
        average_line = average_slope_interception(frame, lines)
        line_image = display_line(average_line, frame)
        combo_image = cv2.addWeighted(frame, .8, line_image, 1,1)
        #plt.imshow(region_of_intrest(combo_image))
        #print('combo_image', combo_image)
        #frames.append(combo_image)
        cv2.imshow('result',combo_image)
        frames.append(combo_image)
        if cv2.waitKey(1) & 0xff == ord('q'):
            break
        #break
cap.release()
for f in frames:
    out.write(f)

out.release()
cv2.destroyAllWindows()



