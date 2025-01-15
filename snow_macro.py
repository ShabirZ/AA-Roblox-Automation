from windowcapture import WindowCapture
from template_match import imageSearch
from imagemask import imageMask
from test_movement import inputAutomation
from objectdetector import objectDetector
import time
import cv2
import copy
import heapq

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
    #cv2.imshow("red", green_objects);cv2.waitKey();cv2.destroyAllWindows()

    largest_red = imageMask(red_objects).largest_island()
    largest_green = imageMask(green_objects).largest_island()
    return largest_red, largest_green

def collapse_1D(cluster, color):
    pixel_map = {}
    for y,x in cluster:
        if x not in pixel_map:
            pixel_map[x] = y
        
        if color == 'Green':
            pixel_map[x] = max(y, pixel_map[x])
        elif color == 'Red':
            pixel_map[x] = min(y, pixel_map[x])
    return pixel_map

def place_units(red_clump, green_clump, movement, window, object_detector):
    OneD_red = collapse_1D(red_clump, 'Red')
    OneD_green = collapse_1D(green_clump, 'Green')
    print(window.w, window.h)
    unit_cords = []
    a = 3
    for _ in range(190):
        seen = set()
        for x,y in OneD_green.items():
            if x//100 in seen:
                continue
            seen.add(x//100)
            new_x, new_y = window.get_screen_position((x,y))
            movement.move_to(new_x, new_y-30)
            movement.press_key('1')
            time.sleep(.5)
            movement.click('left')

            current_screen = window.get_screenshot()
            labels = object_detector.detect(current_screen)
            time.sleep(1)
            for label in labels:
                if label == 3:
                    movement.press_key('q')

                    unit_cords.append((x,y))
                    movement.move_to(100,100)
                    movement.click('left')
                    a-=1
                    if a ==0:
                        return unit_cords
            OneD_green[x] -=30
            time.sleep(1)
    return unit_cords

def temp(movement):
    movement.press_key('1')
    time.sleep(.5)
    movement.click('left')
def main():
    window = WindowCapture('Roblox')
    movement = inputAutomation()
    object_detector = objectDetector()
    time.sleep(3)   
    optimal_rotation(window, movement)
    #path = get_path(window,movement)
    red_clump, green_clump = find_largest_clumps(window, movement)

    unit_cords = place_units(red_clump, green_clump, movement, window, object_detector)
    time.sleep(2)
    for x,y in unit_cords:
        movement.move_to(x,y)

main()