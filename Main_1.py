from Module import adb
from Control import LineageM

class Main():
    def __init__(self, Device_Index, Device_Name):
        self.Device_Index = Device_Index
        self.Device_Name = Device_Name
        self.LM = LineageM.LM(Device_Name,Sample_Path="./Data/Sample_img")


    def start(self):
        while 1:
            try:
                HP_now = self.LM.HP_Detect_Above_80_new(self.Device_Index)
                red_stock = self.LM.Check_Red_Potion(self.Device_Index)
                if HP_now == 0:
                    print('HP Low')
                    if red_stock == 0:
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

            except:
                pass

if __name__ == "__main__":
    obj = Main(Device_Index=2,Device_Name="127.0.0.1:5559") ##home 1-2
    obj.start()
