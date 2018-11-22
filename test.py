import cv2
import numpy as np
def idk(img_aux):
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
	coef_left = np.polyfit(cartesian_left_x, cartesian_left_y, 2)
	polinomy_letf = np.poly1d(coef_left)
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
	coef_right = np.polyfit(cartesian_right_x, cartesian_right_y, 2)
	polinomy_right = np.poly1d(coef_right)
	return polinomy_letf, polinomy_right
def idk_2(img_aux):
	img = img_aux.copy()
	h, w = img.shape
	polinomy_letf, polinomy_right = idk(img)
	for y in range (0, h):
		limit_left = polinomy_letf(h-1-y)
		limit_right =  polinomy_right(h-1-y)
		cv2.imshow('img',img)
		cv2.waitKey(0)
		if(limit_left != limit_right):
			tam_inicial = limit_left-limit_right
			factor = float(w)/float(tam_inicial)
			bigger_img = cv2.resize(img, (int(factor*w), h), 0, 0, interpolation = cv2.INTER_CUBIC)
			for x in range (0, w):
				img[y, x] = bigger_img[y, x+int(factor*(w-1-(limit_left*2))/2.0)]
	return img

img1 = cv2.imread("img.bmp", 0)
img = idk_2(img1)
cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()




