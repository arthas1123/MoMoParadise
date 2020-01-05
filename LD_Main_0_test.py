from Module import ldconsole
from Control import LineageM_LD_test_fn
import time
import keyboard

class Main():
    def __init__(self, Device_Index):
        self.Device_Index = Device_Index
        self.LM = LineageM_LD_test_fn.LM(Index_Num = Device_Index,Sample_Path="./Data/Sample_img")
        self.Safe_Area = self.LM.Safe_Area
        self.LM.Keep_Emu_Img_Cap()
        

    
    def start_battle(self):
        self.LM.Click_System_Btn('Auto')
        time.sleep(0.5)
        while self.LM.Safe_Area != True:
            try:
                HP_now = self.LM.Detect_HP_Above_80()
                self.LM.Detect_PVP()
                org_stock = self.LM.Check_Orange_Potion_low()
                
                if self.LM.PVP_status:
                    self.LM.Click_System_Btn('F1')
                
                elif HP_now == 0:
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
    ### Still in Progress
    def Enter_Dungeon(self):
        self.LM.Click_System_Btn('Menu')
        time.sleep(0.5)
        self.LM.Click_System_Btn('Dungeon')
        time.sleep(0.5)
        ### Select Dungeon 5
        # Dungeon 5 = [1156,330]
        ldconsole.Dnconsole.touch(self.Device_Index,1156,330)
        time.sleep(0.5)
        ### Confirm Dungeon
        ldconsole.Dnconsole.touch(self.Device_Index,754,559)
        ### Wait for loading
        time.sleep(2)
        ### Click Anywhere to continue
        ldconsole.Dnconsole.touch(self.Device_Index,1156,330)
        ### Wait for dungeon initialized
        time.sleep(1)
        self.LM.Click_System_Btn('Auto')
    
    def Auto_Resupply(self):




if __name__ == "__main__":
    obj = Main(Device_Index=1)  ## home 1-2
    time.sleep(1)
    obj.LM.Detect_Potion_Vendor(counts = 2)