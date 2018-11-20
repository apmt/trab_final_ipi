import cv2
import numpy as np
import math
import subprocess
import os
WHITE = 255
BLACk = 0

def gamma_transform(number):
	gamma = 1.5
	const = 1	#Not 0.25 as the paper
	result = 255*const*((number/255)**gamma)
	return result

def local_histogram_equalization_and_gamma_transform(img):
	h, w = img.shape
	img_aux_border = cv2.copyMakeBorder(img,0,8,0,8,cv2.BORDER_CONSTANT,value=0)
	for x in range (0, w, 8):
		for y in range (0, h, 8):
			region = img_aux_border[y:y+8, x:x+8]
			hist_region,bins = np.histogram(region.flatten(),256,[0,256], density=True)
			normalized_CDF_region = hist_region.cumsum()*255
			for p in range (0, 8):
				for q in range (0, 8):
					if(x+p<w and y+q<h):
						img[y+q, x+p] = int(gamma_transform(normalized_CDF_region[region[q, p]]))
	return img

def gaussian_low_pass_filter(img, kernel):
	sigma = kernel/(2*(math.sqrt(2*(math.log(2)))))
	img = cv2.GaussianBlur(img, (kernel, kernel), sigma)
	return img

def average_img (img1, img2, img3, img4):
	img = img1.copy()
	h, w = img.shape
	for x in range (0, w):
		for y in range (0, h):
			pixel = int(img1[y, x])+int(img2[y, x])+int(img3[y, x])+int(img4[y, x])
			pixel /= 4
			img[y, x] = int(pixel)
	return img

def binarization (img):
	cv2.imwrite("aux/gaussian.png", img)
	os.system("mindtct aux/gaussian.png aux/raw_images/raw")
	img_aux = img.copy()
	h, w = img.shape
	brw_file = open("aux/raw_images/raw.brw", "rb")
	for y in range (0, h):
		for x in range (0, w):
			img_aux[y, x] = ord(brw_file.read(1))
	brw_file.close()
	return img_aux

img = cv2.imread("foto.png", 0)
immg = img.copy()
img = local_histogram_equalization_and_gamma_transform(img)
img_kern_3 = gaussian_low_pass_filter(img, 3)
img_kern_5 = gaussian_low_pass_filter(img, 5)
img_kern_7 = gaussian_low_pass_filter(img, 7)
img_kern_9 = gaussian_low_pass_filter(img, 9)
img = average_img(img_kern_3, img_kern_5, img_kern_7, img_kern_9)
img = binarization(img)

cv2.imshow('final',img)
cv2.imwrite("final.png", img)
cv2.waitKey(0)
cv2.destroyAllWindows()