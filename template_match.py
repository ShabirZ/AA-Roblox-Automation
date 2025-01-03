import cv2
import numpy as np
from matplotlib import pyplot as plt
import time



def in_image(img1, upgrade_img): 

    def draw_template_box(method):

        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
    
        cv2.rectangle(img,top_left, bottom_right, 255, 2)
        plt.subplot(121),plt.imshow(res,cmap = 'gray')
        plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(img,cmap = 'gray')
        plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        plt.suptitle(meth)
    
        plt.show()

    img = img1

    template = upgrade_img


    w, h = template.shape[::-1]
    
    # All the 6 methods for comparison in a list
    methods = ['TM_CCOEFF_NORMED','TM_CCORR_NORMED']
    flag = 0

    height, width = img.shape

    top_crop = int(height * 0.2)  # Top 20%
    bottom_crop = int(height * 0.8)  # Bottom 80%

    # Cut the image in half vertically
    img2 = img[top_crop:bottom_crop, : width // 3]
    cv2.imshow('NEW', img2);cv2.waitKey();cv2.destroyAllWindows()
    for meth in methods:
        img = img2.copy()
        method = getattr(cv2, meth)
    
        # Apply template Matching
        res = cv2.matchTemplate(img,template,method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        if max_val >= .8:
            flag+=1
            #draw_template_box(meth)
            #return True
        else:
            print(meth, max_val)
    print(flag)
    return flag ==2





def test():
    images_dir = 'snow_inf_test_img'
    # Specific image paths
    image1_path = "snow_inf_test_img\place_test1.PNG"
    image2_path = "snow_inf_test_img\place_test2.PNG"
    image3_path = "snow_inf_test_img\place_test3.PNG"

    img1,img2,img3 = cv2.imread(image1_path, cv2.IMREAD_GRAYSCALE), cv2.imread(image2_path, cv2.IMREAD_GRAYSCALE),  cv2.imread(image3_path, cv2.IMREAD_GRAYSCALE)
    
    invalid_img1 = "snow_inf_test_img\inf1.PNG"
    invalid_img2 = "snow_inf_test_img\inf2.PNG"
    invalid_img3 = "snow_inf_test_img\place_test3.PNG"
    invalid_images_url = [invalid_img1, invalid_img2, invalid_img3]
    invalid_images = []
    for url in invalid_images_url:
        invalid_images.append(cv2.imread(url, cv2.IMREAD_GRAYSCALE))

    test_imgs = [img1,img2,img3]


    upgrade_path = "snow_inf_test_img\\upgrade_img.PNG"
    first_path = "snow_inf_test_img\\first_img.PNG"
    big_upgrade_path = "snow_inf_test_img\\big_upgrade_delete_template.PNG"

    upgrade_img = cv2.imread(upgrade_path, cv2.IMREAD_GRAYSCALE)
    first_img = cv2.imread(first_path, cv2.IMREAD_GRAYSCALE)
    big_upgrade = cv2.imread(big_upgrade_path, cv2.IMREAD_GRAYSCALE)

    template_imgs = [upgrade_img, first_img]
    
    for img in test_imgs:
        for template in template_imgs:
            print(in_image(img,template))
    print('INVALID: ________________')
    for img in invalid_images:
        for template in template_imgs:
            print(in_image(img,template))
test()
