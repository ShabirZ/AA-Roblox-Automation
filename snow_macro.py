from windowcapture import WindowCapture
from template_match import imageSearch
from imagemask import imageMask
from test_movement import inputAutomation
import time
import cv2

def get_before_after(window, movement):
    prev = imageMask(window.get_screenshot())
    movement.press_key('1')
    post = imageMask(window.get_screenshot())
    movement.press_key('q')
    movement.rotate(.75)

    return prev,post

def green_both(prev, post):
    prev.green_mask()
    post.green_mask()

def main():
    window = WindowCapture('Roblox')
    movement = inputAutomation()
    time.sleep(3)
    largest_count = 0
    direction = 0
    temp = None
    for i in range(4):
        prev,post = get_before_after(window, movement)

        green_both(prev, post)


        green = imageMask.get_hills(prev,post)
        green, curr_count = imageMask(green).largest_hill()
        if curr_count > largest_count:
            temp = green
            largest_count = curr_count
            direction = i

    for _ in range(direction):
        movement.rotate(.75)
    cv2.imshow("before", green);cv2.waitKey();cv2.destroyAllWindows()       
main()