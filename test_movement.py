from pyautogui import *
import autoit
import time

# Move the mouse to x=100, y=200 and click
class inputAutomation:
            
    def move_to(self,x,y):
        autoit.mouse_move(x, y)

    def press_key(self, key):
        autoit.send(key)
        time.sleep(.5)


    def click(self,key):
        autoit.mouse_click(key)

    def rotate(self,x):
        # 3 = 360
        # 1.5 = 180
        # .75  = 90

        autoit.send("{RIGHT Down}")
        time.sleep(x)
        autoit.send("{RIGHT Up}")

