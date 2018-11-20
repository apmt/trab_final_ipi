import glob
import cv2
from func import *

images = glob.glob("Images/*.bmp")
i=1
for image in images:
	img_aux = cv2.imread(image, 0)
	img = img_aux.copy()
	img = local_histogram_equalization_and_gamma_transform(img)
	img_kern_3 = gaussian_low_pass_filter(img, 3)
	img_kern_5 = gaussian_low_pass_filter(img, 5)
	img_kern_7 = gaussian_low_pass_filter(img, 7)
	img_kern_9 = gaussian_low_pass_filter(img, 9)
	img = average_img(img_kern_3, img_kern_5, img_kern_7, img_kern_9)
	img = binarization(img)
	output = np.concatenate((img_aux, img), axis = 1)
	#cv2.imshow('final',img)
	#cv2.waitKey(0)
	#cv2.destroyAllWindows()
	fname='{}{}{}'.format('output/', i, '.bmp')
	cv2.imwrite(fname, output)
	i+=1