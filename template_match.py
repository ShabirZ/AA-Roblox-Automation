import cv2
import numpy as np
from matplotlib import pyplot as plt
import time

def temp(img1, upgrade_img): 
    img = img1

    template = upgrade_img


    w, h = template.shape[::-1]
    
    # All the 6 methods for comparison in a list
    methods = ['TM_CCOEFF', 'TM_CCOEFF_NORMED', 'TM_CCORR',
                'TM_CCORR_NORMED', 'TM_SQDIFF', 'TM_SQDIFF_NORMED']
    img2 = img.copy()
    for meth in methods:
        start = time.time()
        img = img2.copy()
        method = getattr(cv2, meth)
    
        # Apply template Matching
        res = cv2.matchTemplate(img,template,method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    
        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
    
        cv2.rectangle(img,top_left, bottom_right, 255, 2)
        print(time.time() - start)
        plt.subplot(121),plt.imshow(res,cmap = 'gray')
        plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(img,cmap = 'gray')
        plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        plt.suptitle(meth)
    
        plt.show()





def test():
    images_dir = 'snow_inf_test_img'
    # Specific image paths
    image1_path = "snow_inf_test_img\place_test1.PNG"
    image2_path = "snow_inf_test_img\place_test2.PNG"
    image3_path = "snow_inf_test_img\place_test3.PNG"

    img1,img2,img3 = cv2.imread(image1_path, cv2.IMREAD_GRAYSCALE), cv2.imread(image2_path, cv2.IMREAD_GRAYSCALE),  cv2.imread(image3_path, cv2.IMREAD_GRAYSCALE)




    upgrade_path = "snow_inf_test_img\\upgrade_img.PNG"
    first_path = "snow_inf_test_img\\first_img.PNG"
    
    upgrade_img = cv2.imread(upgrade_path, cv2.IMREAD_GRAYSCALE)
    first_img = cv2.imread(first_path, cv2.IMREAD_GRAYSCALE)

    cv2.imshow('NEW2', upgrade_img);cv2.waitKey();cv2.destroyAllWindows()
    cv2.imshow('NEW2', first_img);cv2.waitKey();cv2.destroyAllWindows()

    temp(img1, upgrade_img)


test()
