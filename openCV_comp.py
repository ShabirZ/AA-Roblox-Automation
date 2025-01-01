import cv2
import numpy as np
#from WindowCapture import windowcapture

#robloxCapture = WindowCapture('Roblox')


def green_mask(image):
    #remove all colors except for range of green colors from image
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv,(45, 100, 20), (80, 255, 255) )
    #cv2.imshow("GREEN", mask);cv2.waitKey();cv2.destroyAllWindows()
    return mask

def get_hills(before, after):
    before_mask = green_mask(before)
    after_mask = green_mask(after)  
    cv2.imshow("Before", before_mask);cv2.waitKey();cv2.destroyAllWindows()
    cv2.imshow("After", after_mask);cv2.waitKey();cv2.destroyAllWindows()
    new_green_features = cv2.subtract(after_mask, before_mask)
    cv2.imshow('NEW', new_green_features);cv2.waitKey();cv2.destroyAllWindows()

    #show before, after image
    #show after - before to get possible hills
    return new_green_features

def largest_hill(hills):
    # this function is basically largest island on leetcode
    # however I make it so I return all pixels in the largest Island so i can pick multiple pixels
    def isValidPixel(i,j):
        return 0<=i < len(hills) and 0<= j < len(hills[0]) and hills[i][j] == 255 and (i,j) not in seen
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
    
    def remove_islands(hills, current_hill):
        for x,y in current_hill:
            hills[x][y] = 0
    seen = set()
    temp = np.zeros((len(hills), len(hills[0])))
    #255 = valid pixel
    for i in range(len(hills)):
        for j in range(len(hills[0])):
            if hills[i][j] == 255 and (i,j) not in seen:
                current_hill = find_hill_size(i,j)
                if len(current_hill) > 1000:
                    print(len(current_hill))
                else:
                    remove_islands(hills, current_hill)
                    #if island size too small in pixels black it out
                temp = populate_arr(current_hill, temp)
    return temp

images_dir = 'snow_inf_test_img'
# Specific image paths
image1_path = "snow_inf_test_img\post_hill_test.PNG"
image2_path = "snow_inf_test_img\pre_hill_test_v2.PNG"
image3_path = "snow_inf_test_img\pre_hill_test.PNG"

img1,img2,img3 = cv2.imread(image1_path), cv2.imread(image2_path),  cv2.imread(image3_path)
print('AAAAAAAAA')
green_mask = get_hills(img3, img1) 
print('before')

temp = largest_hill(green_mask)
cv2.imshow('NEW', green_mask);cv2.waitKey();cv2.destroyAllWindows()
#print(temp)
def compare_images(img1,img2):
    pass
    """
    Image Comparison:
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
        #cv2.imshow("Computer Vision". pre_click)
        #cv.imshow("Computer Vision". post_click)
        h, w = img1.shape
        def mse(img1, img2):
            h, w = img1.shape
            diff = cv2.subtract(img1, img2)
            err = np.sum(diff**2)
            mse = err/(float(h*w))
            return mse, diff

        error, diff = mse(img1, img2)
        print("Image matching Error between the two images:",error)

        cv2.imshow("difference", diff)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    """