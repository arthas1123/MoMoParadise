from Module import adb
from Control import  LineageM

class Main():
    def __init__(self):
        self.LM = LineageM.LM(Device_Name="emulator-5554",Sample_Path="./Data/Sample_img")


    def start(self):
        LineageM.LM.Click_System_Btn('Item_Box')
        pass




if __name__ == "__main__":
    obj = Main()
    obj.LM.Click_System_Btn('Item_Box')