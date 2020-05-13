import cv2
import numpy as np
import pytesseract
import tkinter as tk
import os
import os.path
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image
from pytesseract import image_to_string
from pytesseract import Output



srcpath=""

def doesFileExist(filename):
    return os.path.isfile(filename)

def preProcess(imgpath):
    img=cv2.imread(imgpath)
    doesImageExist=doesFileExist(imgpath)
    if doesImageExist==True:
        img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        kernel=np.ones((1,1), np.uint8)
        img=cv2.dilate(img, kernel, iterations=1)
        img=cv2.erode(img, kernel, iterations=1)
        cv2.imwrite(srcpath+ "thresh.png", img)
        #img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    else:
        messageBoxNoImage()
    return img

def drawBoxes(imgpath):
    d = pytesseract.image_to_data(imgpath, output_type=Output.DICT)
    n_boxes = len(d['level'])
    for i in range(n_boxes):
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        cv2.rectangle(imgpath, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imwrite(srcpath+"boxedimg.png",imgpath)

def getText():
    config= ("-psm 3 --oem 1")
    result=pytesseract.image_to_string(Image.open("thresh.png"),config=config)
    file=open("result", "w")
    file.write(result)
    return result

def messageBoxNoImage():
    messagebox.showwarning("Sikertelen művelet","Nem található ilyen nevű kép")

def messageBoxFail():
    messagebox.showwarning("Sikertelen művelet","Sikertelen felismerés")

def messageBoxSuccess():
    messagebox.showinfo("Sikeres művelet","Sikeres felismerés, az eredmény a result fájlba került elmentésre.")

def uploadImage():
    uploadedImgName=filedialog.askopenfile()
    absPath=os.path.abspath(uploadedImgName.name)
    imageName=absPath
    processedImg=preProcess(imageName)
    drawBoxes(processedImg)
    text=getText()
    if text!=None:
        messageBoxSuccess()
    else:
        messageBoxFail()
    print(text)
    

def getImg():
    if imgName.get()!="":
        imageName=imgName.get()
    processedImg=preProcess(imageName)
    if processedImg is not None:
        drawBoxes(processedImg)
        text=getText()
        if text!=None:
            messageBoxSuccess()
        else:
            messageBoxFail()
        print(text)
    else:
        messageBoxNoImage()

if __name__ == "__main__":
    window=tk.Tk()
    tk.Label(window,text="Kép neve kiterjesztéssel").grid(row=0)
    imgName=tk.Entry(window)
    imgName.grid(row=0,column=1)
    window.title("Szövegfelismerő program")
    tk.Button(window,text="Kép feltöltése & felismerés", command=uploadImage).grid(row=1, column=1, sticky=tk.W, pady=4)
    tk.Button(window, text="Felismerés!", command=getImg).grid(row=1, column=0, sticky=tk.W,pady=4)
