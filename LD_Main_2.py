from Module import ldconsole
from Control import LineageM_LD
import time

class Main():
    def __init__(self, Device_Index):
        self.Device_Index = Device_Index
        self.LM = LineageM_LD.LM(Index_Num = Device_Index,Sample_Path="./Data/Sample_img")


    def start(self):
        self.LM.Keep_Emu_Img_Cap()
        time.sleep(0.5)
        while 1:
            try:
                HP_now = self.LM.Detect_HP_Above_80()
                
                org_stock = self.LM.Check_Orange_Potion_low()
                
                if HP_now == 0:
                    print('HP Low')
                    if org_stock == 0:
                        self.LM.Click_System_Btn('F5')
                        time.sleep(0.5)
                    else:
                        print("Orange potion running low")
                        self.LM.Click_System_Btn('F2')
                        break
                elif HP_now == 1:
                    self.LM.Click_System_Btn('F8')
                    time.sleep(0.5)

                else:
                    print("HP High")
                    time.sleep(0.5)
                
                time.sleep(0.5)

            except:
                pass

if __name__ == "__main__":
    obj = Main(Device_Index=2)  ## home 1-2
    #obj = Main(Device_Index=2,Device_Name="127.0.0.1:5559",)  ## ASUS 1-2
    obj.start()
