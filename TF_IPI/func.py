# Modulo de todas as function usadas no programa
import cv2
import numpy as np
import math
import subprocess
import os
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

def gamma_transform(number):
	gamma = 1.5
	const = 1	#Not 0.25 as the paper
	result = 255*const*((number/255)**gamma)
	return result

def local_histogram_equalization_and_gamma_transform(img_aux):
	img = img_aux.copy()
	h, w = img.shape
	# Add border to work on the margin
	img_aux_border = cv2.copyMakeBorder(img,0,8,0,8,cv2.BORDER_CONSTANT,value=0)
	for x in range (0, w, 8):
		for y in range (0, h, 8):
			region = img_aux_border[y:y+8, x:x+8]
			hist_region,bins = np.histogram(region.flatten(),256,[0,256], density=True)
			normalized_CDF_region = hist_region.cumsum()*255
			for p in range (0, 8):
				for q in range (0, 8):
					if(x+p<w and y+q<h):
						# Apply changes already with the gamma transformation
						img[y+q, x+p] = int(gamma_transform(normalized_CDF_region[region[q, p]]))
	return img

def gaussian_low_pass_filter(img_aux, kernel):
	img = img_aux.copy()
	sigma = kernel/(2*(math.sqrt(2*(math.log(2)))))
	img = cv2.GaussianBlur(img, (kernel, kernel), sigma)
	return img

# Usada apenas para testes
def average_img (img1, img2, img3, img4):
	img = img1.copy()
	h, w = img.shape
	for x in range (0, w):
		for y in range (0, h):
			pixel = int(img1[y, x])+int(img2[y, x])+int(img3[y, x])+int(img4[y, x])
			pixel /= 4
			img[y, x] = int(pixel)
	return img

# Threshold das imagens binarizadas
def average_bi (img1, img2, img3, img4):
	white = 255
	black = 0
	img = img1.copy()
	h, w = img.shape
	for x in range (0, w):
		for y in range (0, h):
			brancos = int(img1[y, x])+int(img2[y, x])+int(img3[y, x])+int(img4[y, x])
			brancos /= 255
			# No min 3 ou 4 pretos em comum
			if(brancos <= 2):
				img[y, x] = black
			else:
				img[y, x] = white
	return img

def binarization (img):
	# Cria arquivo auxiliar .jpeg para leitura do mintct
	cv2.imwrite("aux/gaussian.jpeg", img)
	os.system("mindtct aux/gaussian.jpeg aux/raw")
	img_aux = img.copy()
	h, w = img.shape
	# Raw binarized image to cv2_image
	brw_file = open("aux/raw.brw", "rb")
	for y in range (0, h):
		for x in range (0, w):
			img_aux[y, x] = ord(brw_file.read(1))
	brw_file.close()
	return img_aux

# Bilateral 5th degree regression to get left and right polinomials
def get_polynomials(img_aux):
	img = img_aux.copy()
	h, w = img.shape
	# Left polinomial:
	cartesian_left_x = []
	cartesian_left_y = []
	for y in range (0, h):
		for x in range (0, w):
			# first black appearance (left):
			if(img[y, x] == 0):
				cartesian_left_x.append(h-1-y)
				cartesian_left_y.append((w/2)-1-x)
				break
	cartesian_left_x = np.array(cartesian_left_x)
	cartesian_left_y = np.array(cartesian_left_y)
	# 5th degree regression (left)
	coef_left = np.polyfit(cartesian_left_x, cartesian_left_y, 5)
	# Polinomial coefficients (left)
	polinomial_letf = np.poly1d(coef_left)
	# Right polinomial:
	cartesian_right_x = []
	cartesian_right_y = []
	for y in range (0, h):
		for q in range (0, w):
			x= w-1-q
			# first black appearance (right):
			if(img[y, x] == 0):
				cartesian_right_x.append(h-1-y)
				cartesian_right_y.append((w/2)-1-x)
				break
	cartesian_right_x = np.array(cartesian_right_x)
	cartesian_right_y = np.array(cartesian_right_y)
	# 5th degree regression (right)
	coef_right = np.polyfit(cartesian_right_x, cartesian_right_y, 5)
	# Polinomial coefficients (right)
	polinomial_right = np.poly1d(coef_right)
	return polinomial_letf, polinomial_right

def geometry_correction(img_aux):
	img = img_aux.copy()
	h, w = img.shape
	# Getting the 5th degree regressions
	polinomial_letf, polinomial_right = get_polynomials(img)
	# Bicubic interpolation row by row:
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

# Add random ellipses to the image
def add_texture(img_aux):
	img = img_aux.copy()
	h, w = img.shape
	fig, ax = plt.subplots(figsize=[w/100.0, h/100.0])
	fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
	im = ax.imshow(img, cmap='gray')
	NUM = h*w/28
	# Random positions and sizes:
	ells = [Ellipse(xy=(np.random.rand(2) * [w, h]),
					width=np.random.rand() * 5, height=np.random.rand() * 5,
					angle=np.random.rand() * 360, fill=True, color='white')
			for i in range(NUM)]
	# Plotting ellipses:
	for e in ells:
		ax.add_artist(e)
		e.set_clip_box(ax.bbox)
		# Random transparency:
		e.set_alpha(np.random.rand())
	ax.axis('off')
	plt.box(False)
	fig.canvas.draw()
	# Converting matplotlib image to array:
	X = np.array(fig.canvas.renderer._renderer)
	img = X.copy()
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	return img

# Add border fading in order to eliminate odd contours
def add_fade(img_aux):
	img = img_aux.copy()
	h, w = img.shape
	factor = 0.05
	x_limit = int((w*1.0/h)*factor*w)
	y_limit = int(factor*h)
	# Horizontal fade:
	for y in range (0, h):
		for x in range (0, x_limit):
			Dh = (x_limit-x)**2
			img[y, x] = min(img[y, x]+Dh, 255)
			img[y, w-1-x] = min(img[y, w-1-x]+Dh, 255)
	# Vertical fade:
	for x in range (0, w):
		for y in range (0, y_limit):
			Dv = (y_limit-y)**2
			img[y, x] = min(img[y, x]+Dv, 255)
			img[h-1-y, x] = min(img[h-1-y, x]+Dv, 255)
	return img
