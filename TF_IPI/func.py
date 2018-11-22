import cv2
import numpy as np
import math
import subprocess
import os

def gamma_transform(number):
	gamma = 1.5
	const = 1	#Not 0.25 as the paper
	result = 255*const*((number/255)**gamma)
	return result

def local_histogram_equalization_and_gamma_transform(img_aux):
	img = img_aux.copy()
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

def gaussian_low_pass_filter(img_aux, kernel):
	img = img_aux.copy()
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

def average_bi (img1, img2, img3, img4):
	white = 255
	black = 0
	img = img1.copy()
	h, w = img.shape
	for x in range (0, w):
		for y in range (0, h):
			brancos = int(img1[y, x])+int(img2[y, x])+int(img3[y, x])+int(img4[y, x])
			brancos /= 255
			if(brancos <= 2):
				img[y, x] = black
			else:
				img[y, x] = white
	return img

def binarization (img):
	cv2.imwrite("aux/gaussian.jpeg", img)
	os.system("mindtct aux/gaussian.jpeg aux/raw")
	img_aux = img.copy()
	h, w = img.shape
	brw_file = open("aux/raw.brw", "rb")
	for y in range (0, h):
		for x in range (0, w):
			img_aux[y, x] = ord(brw_file.read(1))
	brw_file.close()
	return img_aux

def get_polynomials(img_aux):
	img = img_aux.copy()
	h, w = img.shape
	cartesian_left_x = []
	cartesian_left_y = []
	for y in range (0, h):
		for x in range (0, w):
			if(img[y, x] == 0):
				cartesian_left_x.append(h-1-y)
				cartesian_left_y.append((w/2)-1-x)
				break
	cartesian_left_x = np.array(cartesian_left_x)
	cartesian_left_y = np.array(cartesian_left_y)
	coef_left = np.polyfit(cartesian_left_x, cartesian_left_y, 5)
	polinomial_letf = np.poly1d(coef_left)
	cartesian_right_x = []
	cartesian_right_y = []
	for y in range (0, h):
		for q in range (0, w):
			x= w-1-q
			if(img[y, x] == 0):
				cartesian_right_x.append(h-1-y)
				cartesian_right_y.append((w/2)-1-x)
				break
	cartesian_right_x = np.array(cartesian_right_x)
	cartesian_right_y = np.array(cartesian_right_y)
	coef_right = np.polyfit(cartesian_right_x, cartesian_right_y, 5)
	polinomial_right = np.poly1d(coef_right)
	return polinomial_letf, polinomial_right

def geometry_correction(img_aux):
	img = img_aux.copy()
	h, w = img.shape
	polinomial_letf, polinomial_right = get_polynomials(img)
	for y in range (0, h):
		limit_left = polinomial_letf(h-1-y)
		limit_right =  polinomial_right(h-1-y)
		if(limit_left != limit_right):
			tam_inicial = limit_left-limit_right
			factor = float(w)/float(tam_inicial)
			bigger_img = cv2.resize(img, (int(factor*w), h), 0, 0, interpolation = cv2.INTER_CUBIC)
			for x in range (0, w):
				img[y, x] = bigger_img[y, x+int(factor*(w-1-(limit_left*2))/2.0)]
	return img

def add_texture(img_aux):
	img = img_aux.copy()
	h, w = img.shape
	g_kernel = cv2.getGaborKernel((21, 21), 8.0, np.pi/4, 10.0, 0.5, 0, ktype=cv2.CV_32F)
	img = cv2.filter2D(img, cv2.CV_8UC3, g_kernel)
	return img