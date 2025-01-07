from windowcapture import WindowCapture
from template_match import imageSearch
from imagemask import imageMask
from test_movement import inputAutomation
import time
import cv2
import copy

def get_before_after(window, movement):
    prev = imageMask(window.get_screenshot())
    movement.press_key('1')
    post = imageMask(window.get_screenshot())
    movement.press_key('q')

    return prev,post

def green_both(prev, post):
    prev.green_mask()
    post.green_mask()

def red_both(prev_red,post_red):
    prev_red = prev_red.red_mask()
    post_red = post_red.red_mask()

def get_path(window, movement):
    prev_red, post_red = get_before_after(window,movement)
    red_both(prev_red, post_red)

    red = imageMask.get_hills(prev_red,post_red)
    #cv2.imshow("red", red);cv2.waitKey();cv2.destroyAllWindows()
    red, _ = imageMask(red).largest_hill()
    #cv2.imshow("red", red);cv2.waitKey();cv2.destroyAllWindows()
    return red

def optimal_rotation(window,movement):
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
        movement.rotate(.75)


    for _ in range(direction):
        movement.rotate(.75)

def find_largest_clumps(window, movement):
    prev, post = get_before_after(window,movement)

    prev_red, prev_green = copy.deepcopy(prev), copy.deepcopy(prev)
    post_red, post_green = copy.deepcopy(post), copy.deepcopy(post)
    green_both(prev_green, post_green)
    red_both(prev_red, post_red)
    
    red_objects = imageMask.get_hills(prev_red, post_red)
    green_objects = imageMask.get_hills(prev_green, post_green)
    
    cv2.imshow("red", red_objects);cv2.waitKey();cv2.destroyAllWindows()
    cv2.imshow("green", green_objects);cv2.waitKey();cv2.destroyAllWindows()



    largest_red = imageMask(red_objects).largest_island()
    largest_green = imageMask(green_objects).largest_island()
    return largest_red, largest_green

def main():
    window = WindowCapture('Roblox')
    movement = inputAutomation()
    time.sleep(3)   
    optimal_rotation(window, movement)
    #path = get_path(window,movement)
    red_clump, green_clump = find_largest_clumps(window, movement)

main()