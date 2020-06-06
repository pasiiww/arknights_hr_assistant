import time
import win32gui, win32ui, win32con, win32api
import cv2
import numpy as np
import random

start_ = (423, 527)
size_ = (539, 137)

def window_capture(start_t = start_ ,tag_size = size_):
    hwnd = 0  # 窗口的编号，0号表示当前活跃窗口

    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, tag_size[0], tag_size[1])
    saveDC.SelectObject(saveBitMap)
    start = start_t
    saveDC.BitBlt((0,0), tag_size, mfcDC, start, win32con.SRCCOPY)
    signedIntsArray = saveBitMap.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (tag_size[1],tag_size[0],4)
    mfcDC.DeleteDC()
    saveDC.DeleteDC()
    win32gui.ReleaseDC(hwnd,hwndDC)
    win32gui.DeleteObject(saveBitMap.GetHandle())

    return cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)


def imshow(img):
    cv2.imshow('tt',img)
    while cv2.waitKey() != ord('q'):
        break
    cv2.destroyAllWindows()

single_box_size = (54,163)
x_y = (( 0 , 0 ),
( 0 , 81 ),
( 188 , 0 ),
( 188 , 81 ),
( 377 , 0 ))
def trans_img_2_tagboxes(a):

    tags_boxes = []
    for start_x,start_y in x_y:
            neg_padding = 3
            tag_box = a[start_y + neg_padding:start_y -neg_padding +single_box_size[0] ,start_x +neg_padding:start_x -neg_padding + single_box_size[1],:]
            tag_box= cv2.cvtColor(tag_box,cv2.COLOR_RGB2GRAY)
            ret,tag_box=cv2.threshold(tag_box,170,255,cv2.THRESH_BINARY) #
            tags_boxes.append(tag_box)
            #imshow(tag_box)
    return tags_boxes

tags = {'群攻', 
'生存', '位移', '近战位', '资深干员', 
'爆发', '远程位', '输出', '治疗', 
'快速复活', '削弱', '减速', '新手', 
'召唤', '费用回复', '防护', '支援', 
'高级资深干员', '支援机械', '控场',
'辅助干员', '狙击干员', '术师干员', '重装干员', '近卫干员', '特种干员', '先锋干员', '医疗干员'}    


tags_to_img = np.load('tags.npy')[()]
#tags_to_img = {}
def console_show_img(img):
    #print(img.shape)
    si = img[12:48-12:2,22:157-22:2]
    #imshow(si)
    for i in si:
        for j in i:
            if j == 255:
                print('█',end='')
            else:
                print(' ',end='')
        print('')

def get_text(img):
    maxdelta = 99999999
    name = ""
    for k,vs in tags_to_img.items():
        for v in vs:
            if v.shape != img.shape:
                continue
            delta  = np.abs(np.sum(v - img))
            if delta < maxdelta:
                maxdelta = delta
                name = k
    if maxdelta < 255 * 25:
        return name
    else:
        console_show_img(img)
        name = input("请输入显示的完整的tag内容:").strip()
        while name not in tags:
            name = input("输入有误，请重新输入:").strip()
        if name not in tags_to_img:
            tags_to_img[name] = [img]
        else:
            if len(tags_to_img[name]) < 20:
                tags_to_img[name].append(img)
            else:
                tags_to_img[random.randint(0,19)] = img
        np.save('tags',tags_to_img)
        return name

def get_result():
    a = window_capture()
    a = cv2.resize(a,(539,137))
    graybox = a[93:93 + 30 ,394:394 + 100,:]
    graybox = (graybox > 170)  * (graybox < 180)
    if np.sum(graybox) < 8000:
        return None
    tagboxes = trans_img_2_tagboxes(a) 
    r = []
    for i in tagboxes:
        name = get_text(i)
        r.append(name)
    return r

if __name__ == '__main__':
    print(get_result())

