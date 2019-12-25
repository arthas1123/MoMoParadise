import os
import subprocess
from PIL import ImageGrab
import numpy as np
import win32gui, win32ui, win32con, win32api
from threading import Thread
import time
from PIL import Image
import cv2

class ADB:
    def __init__(self,Device_Name,Screen_Size):

        self.ADB_Path = "./Tool/adb.exe"
        self.Screen_Size = Screen_Size
        self.Device_Name = Device_Name
        self.LD_Path = r"D:\ChangZhi\LDPlayer\\"
        self.Hwnd = 0
        self.ScreenHot = None

    def Keep_Game_ScreenHot(self,Emu_Index,file_name):
        th = Thread(target=self.Keep_Game_ScreenHot_fn,args=[Emu_Index,file_name])
        th.start()

    def Keep_Game_ScreenHot_fn(self,Emu_Index,file_name):
        self.Hwnd = int(self.Get_Self_Hawd(Emu_Index))
    
        while 1:
            
            self.getWindow_Img(self.Hwnd,filename=file_name)
            #self.getWindow_Img(hwnd=self.Hwnd,filename=file_name)
            time.sleep(1)

    def Get_Self_Hawd(self,Index_Num):
        Device_List = self.LD_Call()

        for k, Device_Data in enumerate(Device_List):
            if k != Index_Num:
                continue
            hawd = Device_Data[3]
            return hawd

    def Get_Rect_Img(self,x1,y1,x2,y2):
        pass

    def LD_Call(self):
        File_Path = self.LD_Path + "ldconsole.exe"
        output = subprocess.Popen([File_Path,'list2'],cwd=self.LD_Path,shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        #print(output.stdout.readlines()[0])
        
        
        end = []
        for line in output.stdout.readlines():
            output = line.decode('gbk')
            output = output.strip()
            
            if output != "":
                output = output.split(",")
                end.append(output)
        return end

    def window_capture(self,hwnd,filename):
        game_rect = win32gui.GetWindowRect(int(hwnd))
        # start to modify
        src_image = ImageGrab.grab(game_rect)

        src_image = src_image.resize(self.Screen_Size,Image.ANTIALIAS)
        src_image.save(filename)
        self.ScreenHot = src_image
        # print(type(src_image))
    
    def getWindow_W_H(self,hwnd):
    # 取得目標視窗的大小
        left, top, right, bot = win32gui.GetWindowRect(hwnd)
        width = right - left + 280
        height = bot - top + 150
        return (left, top, width, height)

    def getWindow_Img_new(self,Emu_Index):
        self.Hwnd = int(self.Get_Self_Hawd(Emu_Index))
    
    # 將 hwnd 換成 WindowLong
        s = win32gui.GetWindowLong(self.Hwnd,win32con.GWL_EXSTYLE)
        win32gui.SetWindowLong(self.Hwnd, win32con.GWL_EXSTYLE, s|win32con.WS_EX_LAYERED)
    # 判斷視窗是否最小化
        show = win32gui.IsIconic(self.Hwnd)
    # 將視窗圖層屬性改變成透明    
    # 還原視窗並拉到最前方
    # 取消最大小化動畫
    # 取得視窗寬高
        if show == 1: 
            win32gui.SystemParametersInfo(win32con.SPI_SETANIMATION, 0)
            win32gui.SetLayeredWindowAttributes(self.Hwnd, 0, 0, win32con.LWA_ALPHA)
            win32gui.ShowWindow(self.Hwnd, win32con.SW_RESTORE)    
            x, y, width, height = self.getWindow_W_H(self.Hwnd)        
    # 創造輸出圖層
        hwindc = win32gui.GetWindowDC(self.Hwnd)
        srcdc = win32ui.CreateDCFromHandle(hwindc)
        memdc = srcdc.CreateCompatibleDC()
        bmp = win32ui.CreateBitmap()
    # 取得視窗寬高
        x, y, width, height = self.getWindow_W_H(self.Hwnd)
    # 如果視窗最小化，則移到Z軸最下方
        if show == 1: win32gui.SetWindowPos(self.Hwnd, win32con.HWND_BOTTOM, x, y, width, height, win32con.SWP_NOACTIVATE)
    # 複製目標圖層，貼上到 bmp
        bmp.CreateCompatibleBitmap(srcdc, width, height)
        memdc.SelectObject(bmp)
        memdc.BitBlt((0 , 0), (width, height), srcdc, (8, 3), win32con.SRCCOPY)
    # 將 bitmap 轉換成 np
        signedIntsArray = bmp.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (height, width, 4) #png，具有透明度的
    
    # 釋放device content
        srcdc.DeleteDC()
        memdc.DeleteDC()
        win32gui.ReleaseDC(self.Hwnd, hwindc)
        win32gui.DeleteObject(bmp.GetHandle())
    # 還原目標屬性
        if show == 1 :
            win32gui.SetLayeredWindowAttributes(self.Hwnd, 0, 255, win32con.LWA_ALPHA)
            win32gui.SystemParametersInfo(win32con.SPI_SETANIMATION, 1)
    # 回傳圖片
        src_img = img
        #src_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        #src_img = cv2.imwrite(filename,img)
        self.ScreenHot = src_img
        return src_img

    def Touch(self,x,y,device_name=None):
        if device_name == None:
            device_name = self.Device_Name
        x = str(x)
        y = str(y)
        self.adb_call(device_name,['shell','input','tap',x,y])

    def adb_call(self,device_name,detail_list):
        command = [self.ADB_Path,'-s',device_name]
        for order in detail_list:
            command.append(order)
        print(command)
        subprocess.Popen(command)

    def Drag(self,x1,y1,x2,y2,x3,y3,delay_time=1):
        x1 = x1 * 19199 / self.Screen_Size[0]
        y1 = y1 * 10799 / self.Screen_Size[1]
        x2 = x2 * 19199 / self.Screen_Size[0]
        y2 = y2 * 10799 / self.Screen_Size[1]
        x3 = x3 * 19199 / self.Screen_Size[0]
        y3 = y3 * 10799 / self.Screen_Size[1]

        CREATE_NO_WINDOW = 134217728
        devnull = open(os.devnull, 'w')

        # if os.path.isfile('../Tool/dn_drag.bat') == 1:
        #     print("dndrag存在")
        # else:
        #     print("dndrag不存在")



        main_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

        command = [main_path+'\\Tool\\dn_drag.bat',main_path+"\\Tool\\adb.exe",
                   self.Device_Name, str(x1), str(y1), str(x2), str(y2), str(x3), str(y3), str(delay_time)]

        cmd_str = " ".join(command)
        print(command)


        output = subprocess.Popen(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        print(output.stdout.readlines())
        # os.system(cmd_str)




if __name__ == '__main__':
    obj = ADB(Device_Name="emulator-5554",Screen_Size=[1280,720])
    #print(obj.Hwnd)
    #print(obj.Get_Self_Hawd(0))
    obj.Touch(573,460)
    hawd = obj.Get_Self_Hawd(0)
    
    
    print(hawd)
    im1 = obj.getWindow_Img_new(0)   ## 0
    cv2.imwrite('PVP.jpg',im1)
    #im1 = cv2.imread('test5.jpg')
    #potion_img = im1[598:664, 921:987]
    #cv2.imwrite('orange_potion_low.jpg',potion_img)

    #obj.getWindow_Img(788840,'red_potion_lower.jpg')  ## 1-2
    #obj.getWindow_Img_new(0)
    #obj.Keep_Game_ScreenHot(0,"test4.png")
    # obj.window_capture(hawd,'test.png')
    # obj.Drag(1164,467,1164,400,1164,370)
    # obj.LD_Call()