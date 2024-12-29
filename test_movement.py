from pyautogui import *
import autoit
import time

# Move the mouse to x=100, y=200 and click
time.sleep(2)
def move_to(x,y):
    autoit.mouse_move(x, y)

def press_key(key):
    autoit.send(key)

def click(key):
    autoit.mouse_click(key)

def rotate(x):
    # 3 = 360
    # 1.5 = 180
    # .75  = 90

    autoit.send("{RIGHT Down}")
    time.sleep(x)
    autoit.send("{RIGHT Up}")
time.sleep(1)
#rotate(3)

move_to(500,500)