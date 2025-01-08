from windowcapture import WindowCapture
from template_match import imageSearch
from imagemask import imageMask
from test_movement import inputAutomation
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
    cv2.imshow("gree", green_objects);cv2.waitKey();cv2.destroyAllWindows()



    largest_red = imageMask(red_objects).largest_island()
    largest_green = imageMask(green_objects).largest_island()
    return largest_red, largest_green

def collapse_1D(cluster, color):
    pixel_map = {}
    for x,y in cluster:
        if x not in pixel_map:
            pixel_map[x] = y
        
        if color == 'Green':
            pixel_map[x] = max(y, pixel_map[x])
        elif color == 'Red':
            pixel_map[x] = min(y, pixel_map[x])
    return pixel_map

def euclidean_distance(red_cluster, green_cluster):
    heap = []
    for idx in range(0, len(green_cluster),100):
        x1,y1 = green_cluster[idx]
        shortest_distance = float('inf')
        for x2,y2 in red_cluster:
            shortest_distance = min(shortest_distance, (y2-y1)**2+(x2-x1)**2)
        heapq.heappush(heap, (shortest_distance, x1-10,y1-10))
        if len(heap) > 100:
            heapq.heappop(heap)
    return heap

def temp(movement):
    movement.press_key('1')
    time.sleep(.5)
    movement.click('left')
def main():
    window = WindowCapture('Roblox')
    movement = inputAutomation()
    time.sleep(3)   
    optimal_rotation(window, movement)
    #path = get_path(window,movement)
    red_clump, green_clump = find_largest_clumps(window, movement)
    
    """
    print('start')
    
    closest_pixels = euclidean_distance(red_clump, green_clump)
    print('end')
    for i in range(20):
        distance, x,y = heapq.heappop(closest_pixels)
        movement.move_to(x,y)
        temp(movement)
        time.sleep(2)
    """
main()