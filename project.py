#pip install opencv-python
#pip install pygame
#pip install numpy
from tkinter import *  
import tkinter as tk
import numpy as np
import cv2
import time
import pygame

def write_slogan():
 eye_cas=cv2.CascadeClassifier('haarcascade_eye.xml')
 mouth_cascade = cv2.CascadeClassifier('mouth.xml')
 #hs_cascade = cv2.CascadeClassifier('HS.xml')
 cap=cv2.VideoCapture(0)
 eye_count=0
 mouth_count=0

 def sound_alarm(sound):
    pygame.mixer.init()
    pygame.mixer.music.load(sound)
    pygame.mixer.music.play()

 while True:
    
    ret,frame=cap.read()
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    #cv2.imshow('frame', frame)
    eyes=eye_cas.detectMultiScale(gray,scaleFactor=1.5,minNeighbors=10)
    font = cv2.FONT_HERSHEY_COMPLEX
    cv2.putText(ret, "Panda", (20, 180), font, 18,255)
    for(x,y,w,h) in eyes:
        #time.sleep(.5)
        region_gray=gray[y:y+h,x:x+w]
        img_item='image.png'
        cv2.imwrite(img_item,region_gray)
        clr=(255,0,0)
        stroke=2
        cv2.rectangle(frame,(x,y),(x+w,y+h),clr,stroke)
        #print(eyes)
    if (len(eyes)==0):
            print("closed",eye_count)
            eye_count+=1
            if (eye_count>5):
                print("drowsiness detected")
                sound_alarm("Alert.wav")
                break
    else:
            eye_count=0
        
    mouth_rects = mouth_cascade.detectMultiScale(gray, 1.7, 11)
    for (x,y,w,h) in mouth_rects:
            
            x=int(x+.25*h)
            y=int (y-.25*h)
          #  y = int(y - 0.15*h)
            cv2.rectangle(frame, (x-10,y), (x+w+10,y+h-10), (0,255,0), 3)
            break
    if (len(mouth_rects)==0):
            print("mouth open",mouth_count)
            mouth_count+=1
            if (mouth_count>5):
                print("yawning detected")
                font = cv2.FONT_HERSHEY_COMPLEX
                cv2.putText(ret, "Panda", (20, 180), font, 18,255)
                #cv2.putText(ret, 'Yawning Detected', (10,450), Arial, 3, (0, 255, 0), 2, cv2.LINE_AA)
                sound_alarm("Driver male.wav")
                break
    else:       
                mouth_count=0

   #hs = hs_cascade.detectMultiScale(gray, 1.7, 11)
   #for (x,y,w,h) in hs:
    #        frame=cv2.rectangle(frame, (x,y), (x+w,y+h),0)

            
    cv2.imshow('frame', frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
root = tk.Tk()
root.geometry("450x300")
root.title("Driver Drowsiness")
frame = tk.Frame(root)
frame.pack()

w = Label(root, text="DRIVER DROWSINESS DETECTION SYSTEM ",font=("Helvetica", 16))
w.pack()

w = Label(root, text="USING IMAGE PROCESSING",font=("Helvetica", 16))
w.pack()
bottom = Button(root, text='START', height="2", width="15", fg='black', command=write_slogan).place(x=150, y=100)



bottom1 = Button(root, text='STOP', height="2", width="15", fg='red', command=quit).place(x=150, y=160)



root.mainloop()
