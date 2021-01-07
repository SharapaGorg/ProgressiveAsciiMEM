import sys
import os
import numpy as np

import cv2
import time
import curses
import json

import math
from PIL import Image

gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
gscale2 = '@%#*+=-:. '

cols = 200
scale = 0.43
moreLevels = None

def getAverageL(image):

    im = np.array(image)
    w,h = im.shape

    return np.average(im.reshape(w*h))

def covertImageToAscii(fileName, cols, scale, moreLevels):

    global gscale1, gscale2

    image = Image.open(fileName).convert('L')
    W, H = image.size[0], image.size[1]
    w = W/cols
    h = w/scale

    rows = int(H/h)

    if cols > W or rows > H:
        exit(0)

    aimg = list()

    for j in range(rows):
        y1 = int(j*h)
        y2 = int((j+1)*h)

        if j == rows-1:
            y2 = H

        aimg.append("")

        for i in range(cols):
            x1 = int(i*w)
            x2 = int((i+1)*w)

            if i == cols-1:
                x2 = W

            img = image.crop((x1, y1, x2, y2))
            avg = int(getAverageL(img))

            if moreLevels:
                gsval = gscale1[int((avg*69)/255)]
            else:
                gsval = gscale2[int((avg*9)/255)]

            aimg[j] += gsval

    return aimg

def VideoDivider():
    camera = cv2.VideoCapture("assets\\TMD2.gif")
    i = 0

    while True:
        try:
            f,img = camera.read()
            # cv2.imshow("webcam",img)
            if (cv2.waitKey(5) != -1):
                break

            cv2.imwrite('images_\\{0:05d}.jpg'.format(i),img)
            i += 1

        except Exception as ex:
            break

def show_window(*kwargs):

    string = str()
    
    for i in kwargs:
        for l in i:
            string += l

    start_i, end_i = 0, cols + 1

    for i in range(50):
        stdscr.addstr(i, 0, string[start_i : end_i])
        stdscr.refresh()

        start_i += cols
        end_i += cols

def ASCIIRoat():
    l = 0

    os.chdir("images_")

    for i in os.listdir():

        aimg = covertImageToAscii(i, cols, scale, moreLevels)

        os.chdir("../")
        os.chdir("frames_")

        with open(f"{l}.txt", "w") as file:
            for i in aimg:
                file.write(i)
        l += 1

        os.chdir("../")
        os.chdir("images_")

def main():
    try: os.chdir("frames_") 
    except : pass

    for i in os.listdir():
        with open(i, "r") as f:
            
            file_data = f.readlines()

            show_window(file_data)

            time.sleep(0.05)

os.chdir("images_")

if len(os.listdir()) == 0 :
    os.chdir("../")
    VideoDivider()
else:
    os.chdir("../")

if len(os.listdir("frames_")) == 0:
    ASCIIRoat()

if len(os.listdir()) != 0:

    while 1:
        try:
            stdscr = curses.initscr()
            curses.noecho()
            curses.cbreak()

            main()

            curses.echo()
            curses.nocbreak()
            curses.endwin()  
        except Exception as ex:
            print(ex) 