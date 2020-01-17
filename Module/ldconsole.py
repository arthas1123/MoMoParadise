import os
import shutil
import time
from xml.dom.minidom import parseString
from threading import Thread
import cv2 as cv
import subprocess
import win32gui, win32ui, win32con, win32api
import numpy as np


class DnPlayer(object):
    def __init__(self, info: list):
        super(DnPlayer, self).__init__()
        # 索引，标题，顶层窗口句柄，绑定窗口句柄，是否进入android，进程PID，VBox进程PID
        self.index = int(info[0])
        self.name = info[1]
        self.top_win_handler = int(info[2])
        self.bind_win_handler = int(info[3])
        self.is_in_android = True if int(info[4]) == 1 else False
        self.pid = int(info[5])
        self.vbox_pid = int(info[6])
 
    def is_running(self) -> bool:
        return self.is_in_android
 
    def __str__(self):
        index = self.index
        name = self.name
        r = str(self.is_in_android)
        twh = self.top_win_handler
        bwh = self.bind_win_handler
        pid = self.pid
        vpid = self.vbox_pid
        return "\nindex:%d name:%s top:%08X bind:%08X running:%s pid:%d vbox_pid:%d\n" % (
            index, name, twh, bwh, r, pid, vpid)
 
    def __repr__(self):
        index = self.index
        name = self.name
        r = str(self.is_in_android)
        twh = self.top_win_handler
        bwh = self.bind_win_handler
        pid = self.pid
        vpid = self.vbox_pid
        return "\nindex:%d name:%s top:%08X bind:%08X running:%s pid:%d vbox_pid:%d\n" % (
            index, name, twh, bwh, r, pid, vpid)
 
 
class UserInfo(object):
    def __init__(self, text: str = ""):
        super(UserInfo, self).__init__()
        self.info = dict()
        if len(text) == 0:
            return
        self.__xml = parseString(text)
        nodes = self.__xml.getElementsByTagName('node')
        res_set = [
        #用户信息节点
        ]
        name_set = [
            'id', 'id', 'following', 'fans', 'all_like', 'rank', 'flex',
            'signature', 'location', 'video', 'name'
        ]
        number_item = ['following', 'fans', 'all_like', 'video', 'videolike']
        for n in nodes:
            name = n.getAttribute('resource-id')
            if len(name) == 0:
                continue
            if name in res_set:
                idx = res_set.index(name)
                text = n.getAttribute('text')
                if name_set[idx] not in self.info:
                    self.info[name_set[idx]] = text
                    print(name_set[idx], text)
                elif idx == 9:
                    self.info['videolike'] = text
                elif idx < 2:
                    if len(text) == 0:
                        continue
                    if self.info['id'] != text:
                        self.info['id'] = text
        for item in number_item:
            if item in self.info:
                self.info[item] = int(self.info[item].replace('w', '0000').replace('.', ''))
 
    def __str__(self):
        return str(self.info)
 
    def __repr__(self):
        return str(self.info)



class Dnconsole:
    # 请根据自己电脑配置
    console = 'D:\\Changzhi\\LDPlayer\\ldconsole.exe '
    ld = 'D:\\Changzhi\\LDPlayer\\ld.exe '
    share_path = 'C:\\Users\\Alex\\Documents\\LDPlayer\\Pictures'
     
    @staticmethod
    def get_list():
        cmd = os.popen(Dnconsole.console + 'list2') ##failed due to locale setting, using subprocess to avoid codec issue
        #cmd = subprocess.Popen(Dnconsole.console + 'list2', shell=True, stdin=subprocess.PIPE)
        text = cmd.read()
        cmd.close()
        info = text.split('\n')
        result = list()
        for line in info:
            if len(line) > 1:
                dnplayer = line.split(',')
                result.append(DnPlayer(dnplayer))
        return result
 
    @staticmethod
    def list_running() -> list:
        result = list()
        all = Dnconsole.get_list()
        for dn in all:
            if dn.is_running() is True:
                result.append(dn)
        return result
 
    @staticmethod
    def is_running(index: int) -> bool:
        all = Dnconsole.get_list()
        if index >= len(all):
            raise IndexError('%d is not exist' % index)
        return all[index].is_running()
 
    @staticmethod
    def dnld(index: int, command: str, silence: bool = True):
        cmd = Dnconsole.ld + '-s %d "%s"' % (index, command)
        # print(cmd)
        if silence:
            os.system(cmd)
            return ''
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result
 
    @staticmethod
    def adb(index: int, command: str, silence: bool = False) -> str:
        cmd = Dnconsole.console + 'adb --index %d --command "%s"' % (index, command)
        if silence:
            os.system(cmd)
            return ''
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result
 
    @staticmethod
    def install(index: int, path: str):
        shutil.copy(path, Dnconsole.share_path + str(index) + '/update.apk')
        time.sleep(1)
        Dnconsole.dnld(index, 'pm install /sdcard/Pictures/update.apk')
 
    @staticmethod
    def uninstall(index: int, package: str):
        cmd = Dnconsole.console + 'uninstallapp --index %d --packagename %s' % (index, package)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result
 
    @staticmethod
    def invokeapp(index: int, package: str):
        cmd = Dnconsole.console + 'runapp --index %d --packagename %s' % (index, package)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        print(result)
        return result
 
    @staticmethod
    def stopapp(index: int, package: str):
        cmd = Dnconsole.console + 'killapp --index %d --packagename %s' % (index, package)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result
 
    @staticmethod
    def input_text(index: int, text: str):
        cmd = Dnconsole.console + 'action --index %d --key call.input --value %s' % (index, text)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result
 
    @staticmethod
    def get_package_list(index: int) -> list:
        result = list()
        text = Dnconsole.dnld(index, 'pm list packages')
        info = text.split('\n')
        for i in info:
            if len(i) > 1:
                result.append(i[8:])
        return result
 
    @staticmethod
    def has_install(index: int, package: str):
        if Dnconsole.is_running(index) is False:
            return False
        return package in Dnconsole.get_package_list(index)
 
    @staticmethod
    def launch(index: int):
        cmd = Dnconsole.console + 'launch --index ' + str(index)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result
 
    @staticmethod
    def quit(index: int):
        cmd = Dnconsole.console + 'quit --index ' + str(index)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result
 
    # 设置屏幕分辨率为1080×1920 , dpi = 480
    @staticmethod
    def set_screen_size(index: int):
        cmd = Dnconsole.console + 'modify --index %d --resolution 720,1280,240' % index
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result
 
    @staticmethod
    def touch(index: int, x: int, y: int, delay: int = 0):
        if delay == 0:
            Dnconsole.dnld(index, 'input tap %d %d' % (x, y))
        else:
            Dnconsole.dnld(index, 'input swipe %d %d %d %d %d' % (x, y, x, y, delay))
 
    @staticmethod
    def press_key(index: int, key: int):
        Dnconsole.dnld(index, 'input keyevent %d' % key)
 
    @staticmethod
    def swipe(index, coordinate_leftup: tuple, coordinate_rightdown: tuple, delay: int = 0):
        x0 = coordinate_leftup[0]
        y0 = coordinate_leftup[1]
        x1 = coordinate_rightdown[0]
        y1 = coordinate_rightdown[1]
        if delay == 0:
            Dnconsole.dnld(index, 'input swipe %d %d %d %d' % (x0, y0, x1, y1))
        else:
            Dnconsole.dnld(index, 'input swipe %d %d %d %d %d' % (x0, y0, x1, y1, delay))
 
    @staticmethod
    def copy(name: str, index: int = 0):
        cmd = Dnconsole.console + 'copy --name %s --from %d' % (name, index)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result
 
    @staticmethod
    def add(name: str):
        cmd = Dnconsole.console + 'add --name %s' % name
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result
 
    @staticmethod
    def auto_rate(index: int, auto_rate: bool = False):
        rate = 1 if auto_rate else 0
        cmd = Dnconsole.console + 'modify --index %d --autorotate %d' % (index, rate)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result
 
    @staticmethod
    def change_device_data(index: int):
        # 改变设备信息
        cmd = Dnconsole.console + 'modify --index %d --imei auto --imsi auto --simserial auto --androidid auto --mac auto' % index
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result
 
    @staticmethod
    def change_cpu_count(index: int, number: int):
        # 修改cpu数量
        cmd = Dnconsole.console + 'modify --index %d --cpu %d' % (index, number)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result
 
    @staticmethod
    def get_activity_name(index: int):
        text = Dnconsole.dnld(index, 'dumpsys activity top | grep ACTIVITY', False)
        text = text.split(' ')
        for i, s in enumerate(text):
            if len(s) == 0:
                continue
            if s == 'ACTIVITY':
                return text[i + 1]
        return ''
 
    @staticmethod
    def wait_activity(index: int, activity: str, timeout: int) -> bool:
        for i in range(timeout):
            if Dnconsole.get_activity_name(index) == activity:
                return True
            time.sleep(1)
        return False
 
    @staticmethod
    def find_pic(screen: str, template: str, threshold: float):
        try:
            scr = cv.imread(screen)
            tp = cv.imread(template)
            result = cv.matchTemplate(scr, tp, cv.TM_SQDIFF_NORMED)
        except cv.error:
            print('File error：', screen, template)
            time.sleep(1)
            try:
                scr = cv.imread(screen)
                tp = cv.imread(template)
                result = cv.matchTemplate(scr, tp, cv.TM_SQDIFF_NORMED)
            except cv.error:
                return False, None
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        if min_val > threshold:
            print(template, min_val, max_val, min_loc, max_loc)
            return False, None
        print(template, min_val, min_loc)
        return True, min_loc
 
    @staticmethod
    def wait_picture(index: int, timeout: int, template: str) -> bool:
        count = 0
        while count < timeout:
            Dnconsole.dnld(index, 'screencap -p /sdcard/Pictures/apk_scr.png')
            time.sleep(2)
            ret, loc = Dnconsole.find_pic(Dnconsole.share_path + '%d/apk_scr.png' % index, template, 0.001)
            if ret is False:
                print(loc)
                time.sleep(2)
                count += 2
                continue
            print(loc)
            return True
        return False
 
    # 在当前屏幕查看模板列表是否存在,是返回存在的模板,如果多个存在,返回找到的第一个模板
    @staticmethod
    def check_picture(index: int, templates: list):
        Dnconsole.dnld(index, 'screencap -p /sdcard/Pictures/apk_scr.png')
        time.sleep(1)
        for i, t in enumerate(templates):
            ret, loc = Dnconsole.find_pic(Dnconsole.share_path + '%d/apk_scr.png' % index, t, 0.001)
            if ret is True:
                return i, loc
        return -1, None
    
    @staticmethod
    def get_list_info(index: int):
        cmd = os.popen(Dnconsole.console + 'list2') ##failed due to locale setting, using subprocess to avoid codec issue
        #cmd = subprocess.Popen(Dnconsole.console + 'list2', shell=True, stdin=subprocess.PIPE)
        text = cmd.read()
        cmd.close()
        info = text.split('\n')
        result = list()
        for line in info:
            if len(line) > 1:
                dnplayer = line.split(',')
                result.append(dnplayer)
        return result[index]

    @staticmethod
    def getWindow_W_H(hwnd):
    # 取得目標視窗的大小
        left, top, right, bot = win32gui.GetWindowRect(hwnd)
        width = right - left + 280
        height = bot - top + 150
        return (left, top, width, height)


    @staticmethod
    def getWindow_Img_new(Emu_Index: int):
        Hwnd = int(Dnconsole.get_list_info(Emu_Index)[3])
    # 將 hwnd 換成 WindowLong
        s = win32gui.GetWindowLong(Hwnd,win32con.GWL_EXSTYLE)
        win32gui.SetWindowLong(Hwnd, win32con.GWL_EXSTYLE, s|win32con.WS_EX_LAYERED)
    # 判斷視窗是否最小化
        show = win32gui.IsIconic(Hwnd)
    # 將視窗圖層屬性改變成透明    
    # 還原視窗並拉到最前方
    # 取消最大小化動畫
    # 取得視窗寬高
        if show == 1: 
            win32gui.SystemParametersInfo(win32con.SPI_SETANIMATION, 0)
            win32gui.SetLayeredWindowAttributes(Hwnd, 0, 0, win32con.LWA_ALPHA)
            win32gui.ShowWindow(Hwnd, win32con.SW_RESTORE)    
            x, y, width, height = Dnconsole.getWindow_W_H(Hwnd)        
    # 創造輸出圖層
        hwindc = win32gui.GetWindowDC(Hwnd)
        srcdc = win32ui.CreateDCFromHandle(hwindc)
        memdc = srcdc.CreateCompatibleDC()
        bmp = win32ui.CreateBitmap()
    # 取得視窗寬高
        x, y, width, height = Dnconsole.getWindow_W_H(Hwnd)
    # 如果視窗最小化，則移到Z軸最下方
        if show == 1: win32gui.SetWindowPos(Hwnd, win32con.HWND_BOTTOM, x, y, width, height, win32con.SWP_NOACTIVATE)
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
        win32gui.ReleaseDC(Hwnd, hwindc)
        win32gui.DeleteObject(bmp.GetHandle())
    # 還原目標屬性
        if show == 1 :
            win32gui.SetLayeredWindowAttributes(Hwnd, 0, 255, win32con.LWA_ALPHA)
            win32gui.SystemParametersInfo(win32con.SPI_SETANIMATION, 1)
    # 回傳圖片
        cv.imwrite('Emu_'+ str(Emu_Index) + '_now.jpg',img)
        return img

if __name__ == "__main__":
    #print(Dnconsole.console)
    a = Dnconsole()
    
    globals.initialize()
    a.getWindow_Img_new(0)
    #time.sleep(5)
    globals.stop_cap = True
    
    #print("killed")
    #print(res.shape)
    #a.screen_now = a.getWindow_Img_new(1)
    #print(a.screen_now)

    #print(a.bind_win_handler)
    #res = Dnconsole.get_list()
    #print(type(res))