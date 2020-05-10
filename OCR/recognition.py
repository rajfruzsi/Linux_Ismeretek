import cv2
import numpy as np
import pytesseract
import tkinter as tk
import os
from tkinter import filedialog
from PIL import Image
from pytesseract import image_to_string
from pytesseract import Output

imageName=""

srcpath=""
imgname="test.jpg"
imageName=""


def preproc(imgpath):
    img=cv2.imread(imgpath)
    img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kernel=np.ones((1,1), np.uint8)
    img=cv2.dilate(img, kernel, iterations=1)
    img=cv2.erode(img, kernel, iterations=1)
    cv2.imwrite(srcpath+ "thresh.png", img)
    #img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    return img

def boxes(imgpath):
    d = pytesseract.image_to_data(imgpath, output_type=Output.DICT)
    n_boxes = len(d['level'])
    for i in range(n_boxes):
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        cv2.rectangle(imgpath, (x, y), (x + w, y + h), (0, 255, 0), 2)

    
    
def getText():
    config= ("-psm 3 --oem 1")
    print("gettext")
    result=pytesseract.image_to_string(Image.open("thresh.png"),config=config)
    file=open("result", "w")
    file.write(result)
    return result

def uploadImage():
    uploadedImgName=filedialog.askopenfile()
    absPath=os.path.abspath(uploadedImgName.name)
    imageName=absPath
    print(absPath)
    processedImg=preproc(imageName)
    boxes(processedImg)
    print("fgvelott")
    text=getText()
    print(text)
    

def getImg():
    if imgName.get()!="":
        imageName=imgName.get()
    processedImg=preproc(imageName)
    boxes(processedImg)
    text=getText()
    print(text)
    print("juhu")


window=tk.Tk()
tk.Label(window,text="Kép neve kiterjesztéssel").grid(row=0)
imgName=tk.Entry(window)
imgName.grid(row=0,column=1)
window.title("Szövegfelismerő program")
tk.Button(window,text="Kép feltöltése & felismerés", command=uploadImage).grid(row=2, column=0, sticky=tk.W, pady=4)
tk.Button(window, text="Felismerés!", command=getImg).grid(row=1, column=0, sticky=tk.W,pady=4)


