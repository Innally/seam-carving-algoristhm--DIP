# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 Double Shift 在所有地方搜索类、文件、工具窗口、操作和设置。

import numpy as np
import cv2 as cv

win=5
def preprocess(img):
    """
    :param img:
    :return:
    get the energy of the img
    """
    grey=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    # get the sobel of x and y orientation
    sobx=cv.Sobel(grey,ddepth=-1,dx=1,dy=0,ksize=3)
    soby=cv.Sobel(grey,ddepth=-1,dx=0,dy=1,ksize=3)
    # calculate the energy
    energy=sobx+soby
    return energy

def seamH(energy,h,w):
    """
    :param energy: energy of a image
    :param h: the height of the image
    :param w: width of the image
    :return: a seam
    """
    minE=min(energy[0,:]+energy[1,:])
    gate=list(energy[0,:]+energy[1,:]).index(minE)
    seam=[(0,gate)]
    last=gate
    for i in range(1,h):
        temp = 256
        tempj=-1
        if i == 60:
            print(60)
        # get the least energy from every line
        for j in range(-win,win+1):
            tj=last+j
            if tj<0 or tj>w:
                continue
            elif energy[i,tj]<temp:

                temp=energy[i,tj]
                tempj=tj
        seam.append((i,tempj))
    return seam

def carveH(img,seam):
    """
    :param img: raw image
    :param seam: seam to remove of
    :return: new image and new energy
    """
    h,w,c=img.shape
    w-=1
    newimg=np.zeros((h,w,c),dtype='uint8')
    for p in seam:
        if p[1]==0:
            newimg[p[0], 0:, :] = img[p[0], 1:, :]
        elif p[1]==w+1:
            newimg[p[0], 0:w, :] = img[p[0], 0:w, :]
        else:
            newimg[p[0],0:p[1],:]=img[p[0],0:p[1],:]
            newimg[p[0],p[1]:,:]=img[p[0],p[1]+1:,:]
    # cv.imshow('new',newimg)
    # cv.waitKey(0)
    energy=preprocess(newimg)
    return newimg,energy


def seamW(energy,h,w):
    minE = min(energy[:, 0] + energy[:, 1]);
    gate = list(energy[:,0] + energy[:,1]).index(minE)
    seam = [(gate,0)]
    last = gate
    for i in range(1, w):
        temp = 256
        tempj = -1
        # get the least energy from every line
        for j in range(-win, win+1):
            tj = last + j
            if tj < 0 or tj > h:
                continue
            elif energy[tj, i] < temp:
                temp = energy[tj, i]
                tempj = tj
        seam.append((tempj, i))
    return seam


def carveW(img,seam):
    h, w, c = img.shape
    h -= 1
    newimg = np.zeros((h, w, c), dtype='uint8')
    for p in seam:
        if p[0] == 0:
            newimg[0:, p[1], :] = img[1:, p[1], :]
        elif p[1] == h + 1:
            newimg[0:, p[1], :] = img[0:h, p[1], :]
        else:
            newimg[0:p[0], p[1], :] = img[0:p[0], p[1], :]
            newimg[p[0]:, p[1], :] = img[p[0]+1:, p[1], :]
    # cv.imshow('new', newimg)
    # cv.waitKey(0)
    energy = preprocess(newimg)
    return newimg, energy


if __name__ == '__main__':
    img=cv.imread("test.jpg")

    energy=preprocess(img)
    h,w=energy.shape

    # input the parameter1
    n = input("How many Seams do you wanna remove?")
    mode=input("Do you wanna carve from height or weight?(input 1 for height, 2 for width)")
    # mode=1
    # calculate the carving seam
    # mode 1 is to remove from column
    if mode=='1':
        for i in range(int(n)):
            seam=seamH(energy,h=h,w=w)
            # print(seam)
            img,energy=carveH(img,seam)
            h, w = energy.shape

        cv.imshow("result",img)
        cv.waitKey(0)

    # mode 2 is to remove from row
    elif mode=='2':
        for i in range(int(n)):
            seam = seamW(energy, h=h, w=w)
            # print(seam)
            img, energy = carveW(img, seam)
            h, w = energy.shape

        cv.imshow("result", img)
        cv.waitKey(0)
    else:
        print("No such mode")


