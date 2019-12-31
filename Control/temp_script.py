    ### HP_Detection_Field_Test:
    while 1:
        try:
            result = obj.HP_Detect_Above_80_new(0)
        
            if result == 1:
                print("Poisoned")
                obj.Click_System_Btn('F2')

            elif result == 0:
                print("HP below 80%")
                obj.Click_System_Btn('F5')
            
            else:
                print("Good!")
        
            time.sleep(0.5)
        except:
            pass
    ### Potion_Detection_Test:
    while 1:
        Has_stat =   obj.Check_Red_Water_Exist()
        if Has_stat == 1:
            print("有藥水")
        else:
            print("沒藥水")
            obj.Click_System_Btn("F8")
        time.sleep(1)
## eggroll
    while 1:
        try:
            HP_now = obj.HP_Detect_Above_80_new(0)
            org_stock = obj.Check_Orange_Potion(0)
            if HP_now == 0:
                print('HP Low')
                if org_stock == 0:
                    obj.Click_System_Btn('F5')
                    time.sleep(0.5)
                else:
                    print("Orange potion running low")
                    obj.Click_System_Btn('F2')
                    break

            else:
                print("HP High")
                time.sleep(0.5)

        except:
            pass

### Hint of interrupt
import threading as th

keep_going = True
def key_capture_thread():
    global keep_going
    input()
    keep_going = False

def do_stuff():
    th.Thread(target=key_capture_thread, args=(), name='key_capture_thread', daemon=True).start()
    while keep_going:
        print('still going...')

do_stuff()