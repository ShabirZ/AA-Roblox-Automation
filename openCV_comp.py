import cv2
import numpy as np
import time # meant for benchmarking

#from WindowCapture import windowcapture

#robloxCapture = WindowCapture('Roblox')

class imageMask:
    def __init__(self, img):
        self.img = img
        
    def green_mask(self):
        #remove all colors except for range of green colors from image
        hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)
        self.img = cv2.inRange(hsv,(45, 100, 20), (80, 255, 255) )
        #cv2.imshow("GREEN", mask);cv2.waitKey();cv2.destroyAllWindows()

    def red_mask(self):
        hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)
        self.img = cv2.inRange(hsv,(150, 100, 20), (180, 255, 255) )
        #cv2.imshow("GREEN", mask);cv2.waitKey();cv2.destroyAllWindows()
    
    @staticmethod
    def get_hills(before, after):
        #the way this function works is it takes two green masks (before and after) and subtracts them to get proper hills

        #before_mask = green_mask(before)
        #after_mask = green_mask(after)  
        #cv2.imshow("Before", before_mask);cv2.waitKey();cv2.destroyAllWindows()
        #cv2.imshow("After", after_mask);cv2.waitKey();cv2.destroyAllWindows()

        new_green_features = cv2.subtract(after.img, before.img)

        #show before, after image
        #show after - before to get possible hills

        #look into bitwise not instead of this (may save computation?)
        #https://stackoverflow.com/questions/59012898/filter-out-everything-of-a-certain-color-using-opencv
        return new_green_features

    def largest_hill(self):
        # this function is basically largest island on leetcode
        # however I make it so I return all pixels in the largest Island so i can pick multiple pixels
        def isValidPixel(i,j):
            return 0<=i < len(self.img) and 0<= j < len(self.img[0]) and self.img[i][j] == 255 and (i,j) not in seen
        def find_hill_size(i,j):
            stack = [(i,j)]
            axis = [(1,0), (0,1), (-1,0), (0,-1)]
            current_hill = []
            while stack:
                x,y = stack.pop()
                for x_delta, y_delta in axis:
                    r,c = x+x_delta, y+ y_delta
                    if isValidPixel(r,c):
                        stack.append([r,c])
                        seen.add((r,c))
                        current_hill.append((r,c))
            return current_hill
        def populate_arr(current_hill, temp):
            for pixel_x, pixel_y in current_hill:
                temp[pixel_x][pixel_y] = len(current_hill)
            return temp
        
        def remove_islands(image, current_hill):
            for x,y in current_hill:
                image[x][y] = 0
        seen = set()
        temp = np.zeros((len(self.img), len(self.img[0])))
        #255 = valid pixel
        for i in range(len(self.img)):
            for j in range(len(self.img[0])):
                if self.img[i][j] == 255 and (i,j) not in seen:
                    current_hill = find_hill_size(i,j)
                    if len(current_hill) < 1000:
                        remove_islands(self.img, current_hill)
                        #if island size too small in pixels black it out
        
        #right now this function updates the current image and deletes small clumps
        #thinking of making array of large clumps (like a heap that points to clump to put unit on largest clump)
        # looks better visually, bad in terms of speed i think
        return self.img




def test():
    images_dir = 'snow_inf_test_img'
    # Specific image paths
    image1_path = "snow_inf_test_img\post_hill_test.PNG"
    image2_path = "snow_inf_test_img\pre_hill_test_v2.PNG"
    image3_path = "snow_inf_test_img\pre_hill_test.PNG"

    img1,img2,img3 = cv2.imread(image1_path), cv2.imread(image2_path),  cv2.imread(image3_path)
    before = imageMask(img3)
    after = imageMask(img1)

    before.green_mask()
    after.green_mask()

    green_mask = imageMask.get_hills(before,after)

    green_mask = imageMask(green_mask)

    cv2.imshow('Before', before.img);cv2.waitKey();cv2.destroyAllWindows()
    cv2.imshow('After', after.img);cv2.waitKey();cv2.destroyAllWindows()
    cv2.imshow('Greem', green_mask.img);cv2.waitKey();cv2.destroyAllWindows()
    green_mask.largest_hill()
    cv2.imshow('Greenv2', green_mask.img);cv2.waitKey();cv2.destroyAllWindows()


    """
    print('AAAAAAAAA')
    green_mask = get_hills(img3, img1) 
    print('before')
    temp, temp2 = largest_hill(green_mask) # takes .6 seconds to run (can optomize by shrinking screen to only look at middle)
    cv2.imshow('NEW', temp);cv2.waitKey();cv2.destroyAllWindows()
    cv2.imshow('NEW2', temp2);cv2.waitKey();cv2.destroyAllWindows()
    """
test()