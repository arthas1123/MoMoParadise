#from Module import adb
import  adb
import time
import os
from PIL import Image
import imagehash
import cv2
import numpy as np


class LM:
    def __init__(self,Device_Name,Sample_Path):
       self.ADB = adb.ADB(Device_Name=Device_Name,Screen_Size=[1280,720])
       #啟動截圖線程
       self.Game_Screen = self.ADB.ScreenHot
       self.Sample_Image = dict()
       #導入範例檔案
       self.Import_Sample_Image(Sample_Path)

       #  self.ADB.Keep_Game_ScreenHot(Emu_Index=0,file_name='test.jpg')

       #  while self.ADB.ScreenHot == None:
           #  print("等待…")
           #  time.sleep(0.1)

    def Image_CMP(self,sample_img_name,source_img):
        Sample_img = Image.open(self.Sample_Image[sample_img_name])
        Sample_hash = imagehash.phash(Sample_img)

        source_hash = imagehash.phash(source_img)

        Point = Sample_hash - source_hash

        return Point
    def Image_CMP_new(self,temp_img,threshold,Emu_Index):
        img_src = self.ADB.getWindow_Img_new(Emu_Index)
        #cv2.imwrite('src1.jpg',img_src)
        im1 = cv2.cvtColor(img_src, cv2.COLOR_BGRA2BGR)
        #cv2.imwrite('src2.jpg',img_src)
        template = cv2.imread(temp_img)
        #print(template.shape)
        
        res = cv2.matchTemplate(im1, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        cv2.imwrite('img_cmp.jpg',img_src)
        cv2.imwrite('temp.jpg',template)
        print(max_val)
        
        if max_val > threshold:
            return max_loc
        else:
            print('Not found')
            return 0


    def HP_Detect_Above_80(self,source_img):
        # Lineage M HP : Top-Left = [74,17], Bot-Right = [264,29]
        # length = 190, width = 12
        # 90% = 74 + 190 * 0.9 => [245,23]
        # 80% => [226, 23]
        # 70% => [207, 23]
        # 60% => [188, 23]
        # 50% => [169, 23]
        # 40% => [150, 23]
        
        im_source = cv2.imread(source_img)
        im_HSV = cv2.cvtColor(im_source,cv2.COLOR_BGR2HSV)
        
        # Red Mask
        lower_red = np.array([0,43,46]) 
        upper_red = np.array([10,255,255])
        mask = cv2.inRange(im_HSV, lower_red, upper_red)

        if mask[23,226] == 255:
            return 1
        else:
            return 0


    def HP_Detect_Above_80_new(self,Emu_Index):
        # Lineage M HP : Top-Left = [74,17], Bot-Right = [264,29]
        # length = 190, width = 12
        # 90% = 74 + 190 * 0.9 => [245,23]
        # 80% => [226, 23]
        # 70% => [207, 23]
        # 60% => [188, 23]
        # 50% => [169, 23]
        # 40% => [150, 23]
        
        src_img = self.ADB.getWindow_Img_new(Emu_Index)
        im_HSV = cv2.cvtColor(src_img, cv2.COLOR_BGR2HSV)
        
        # Red Mask
        lower_red = np.array([0,43,150]) 
        upper_red = np.array([10,255,255])
        red_mask = cv2.inRange(im_HSV, lower_red, upper_red)
        # test if HP is correctly filtered
        res_img = cv2.imwrite('res.jpg',red_mask)

        
        # Green Mask
        lower_green = np.array([50,43,46]) 
        upper_green = np.array([70,255,255])
        green_mask = cv2.inRange(im_HSV, lower_green, upper_green)

        if green_mask[23,112] == 255:
            return 1 # green, poisoned
        elif red_mask[23,226] == 255:
            return 2 # HP above 80%
        else:
            return 0 # gray

    def PIL_to_CV2(self,Pil_Img):
        open_cv_image = np.array(Pil_Img)
        open_cv_image = open_cv_image[:, :, ::-1].copy()
        return open_cv_image

    def Get_Array_Num_Count(self,NP_Arr,Num):
        rs = np.where(NP_Arr==Num)
        #print(rs)
        k = 0
        for row in rs:
            for n in row:
                 k +=1

        return k

    def Check_Sign_in_Red_Point(self):
        loc = [1017,303,1035,328]
        Mail_Box_Img = self.ADB.ScreenHot.crop(loc)
        Mail_Box_Img.save('now_Sign_In_Point.png')

        W_count = self.Get_PIL_Red_Point_Count(Mail_Box_Img)
        if W_count == 0:
            return 0
        else:
            return 1


    def Check_MailBox_Red_Point(self):
        # loc = [1093,156,1113,183]
        loc = [1093, 156, 1133, 203]
        Mail_Box_Img =  self.ADB.ScreenHot.crop(loc)
       # Mail_Box_Img.save('now_main_box.png')

        W_count = self.Get_PIL_Red_Point_Count(Mail_Box_Img)
        if W_count == 0:
            return 0
        else:
            return 1




    #取得pil格式圖片的紅色點數量
    def Get_PIL_Red_Point_Count(self,PIL_Img):
        CV2_Image = self.PIL_to_CV2(PIL_Img)
        HSV = cv2.cvtColor(CV2_Image, cv2.COLOR_BGR2HSV)

        # 過濾出指定的顏色
        low_range = np.array([0, 123, 100])
        high_range = np.array([5, 255, 255])
        mask = cv2.inRange(HSV, low_range, high_range)

        W_count = self.Get_Array_Num_Count(mask, 255)
        return W_count

    def Check_Menu_Red_Point(self):
        loc = [1243,21,1261,40]

        Menu_img = self.ADB.ScreenHot.crop(loc)
       # Menu_img.save('now_menu.png')

        W_count = self.Get_PIL_Red_Point_Count(Menu_img)
        if W_count == 0:
            return  0
        else:
            return 1

    def Import_Sample_Image(self,Path):
        if os.path.isdir(Path) == False:
            print("範例圖片資料夾不存在")
            return 0
        File_List = os.listdir(Path)

        for File_Name in File_List:
            File_Index = File_Name.replace(".png","")
            self.Sample_Image[File_Index] = Path+"/"+ File_Name

        print("範例圖片導入成功")


    def Check_Red_Water_Exist(self):
        Red_W = self.ADB.ScreenHot.crop((222,18,260,56))
        Red_W.save("now_water.png")
        Point = self.Image_CMP("red_water_zero",Red_W)
        if Point == 0:
            return 0
        else:
            return 1
    
    def Check_Orange_Potion(self,Emu_Index):
        org_loc = self.Image_CMP_new(temp_img = 'orange_potion_low.jpg', threshold = 0.99, Emu_Index =0)
        if org_loc[0] in range(921,987):
            print('Low')
        else:
            print('Good')

    def Check_And_Take_Sign_MailBox(self):

        if self.Check_Menu_Red_Point() == 1:
            self.Click_System_Btn("Menu")
            time.sleep(1.5)
            if self.Check_MailBox_Red_Point() == 1:
                print("有新郵件")
                self.Click_System_Btn("Menu_Sign_in")
                time.sleep(0.5)
                self.Click_System_Btn("Menu_Sign_in")
                time.sleep(1.5)
            if self.Check_Sign_in_Red_Point() == 1:
                print("還沒簽到")
                self.Click_System_Btn("Menu_Mail_Box")
                time.sleep(0.5)
                self.Click_System_Btn("Menu_Mail_Box_All_Taken")
                time.sleep(0.3)
                self.Click_System_Btn("Menu")
                time.sleep(1.5)
            self.Click_System_Btn("Menu")


    def Click_System_Btn(self,name):
        Btn_Map = {}
        Btn_Map['F1'] = [544, 637]
        Btn_Map['F2'] = [620, 637]
        Btn_Map['F3'] = [706, 637]
        Btn_Map['F4'] = [784, 637]
        Btn_Map['F5'] = [960, 637]
        Btn_Map['F6'] = [1047, 637]
        Btn_Map['F7'] = [1125, 637]
        Btn_Map['F8'] = [1203, 637]
        Btn_Map['Auto'] = [970, 512]
        Btn_Map['Self'] = [1060, 402]
        Btn_Map['Pick_up'] = [1168, 429]
        Btn_Map['Attack'] = [1104, 520]
        Btn_Map['Store'] = [935, 45]
        Btn_Map['Item_Box'] = [1009, 45]
        Btn_Map['Skill'] = [1080, 45]
        Btn_Map['Mission'] = [1161, 45]
        Btn_Map['Mission_Close_Menu'] = [1237, 45]
        Btn_Map['Menu'] = [1237, 45]
        Btn_Map['Menu_Sign_in'] = [1082, 185]
        Btn_Map['Menu_Mail_Box'] = [1006, 327]
        Btn_Map['Menu_Mail_Box_All_Taken'] = [1084, 662]




        if name not in Btn_Map:
            print("無此按鍵名稱：{}".format(name))
            return 0

        click_loc = Btn_Map[name]
        self.ADB.Touch(click_loc[0],click_loc[1])



if __name__ == '__main__':
    obj = LM(Device_Name="emulator-5554",Sample_Path="./Data/Sample_img")
    #obj.Image_CMP_new('orange_potion_low.jpg',0.9,0)
    #obj.Check_Orange_Potion(0)
    print(obj.HP_Detect_Above_80_new(0))

    ### HP_Detection_Test:
    #if obj.HP_Detect_Above_80('test.png'):
        #print('HP above 80%')
    #else:
        #print('HP below 80%')
    


    # obj.Click_System_Btn("Menu_Sign_in")
    # rs = obj.Check_And_Take_Sign_MailBox()

    # if rs == 1:
    #     print("有新訊息哦")
    # else: 
    #     print("沒有新訊息哦")

    # obj.Click_System_Btn('Menu')
    # time.sleep(0.2)

    # obj.Import_Sample_Image("../Data/Sample_img")

    # obj.Image_Hash(obj.ADB.ScreenHot)

    #obj.Get_Red_Water_Img()
    #
    #obj.Click_System_Btn('Item_Box')
    # time.sleep(0.2)
    # obj.Click_System_Btn('Pick_up')
    # time.sleep(0.2)
    # obj.Click_System_Btn('Attack')

