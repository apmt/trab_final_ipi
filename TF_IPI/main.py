import glob
import cv2
from func import *

# Recebe todas imagens
images = glob.glob("Images/*.bmp")
index = 1

# Para cada imagem:
for image in images:
	# Le imagem
	img = cv2.imread(image, 0)
	# Processamentos iniciais(local hitogram equalization and gamma transform):
	img_eq_gam = local_histogram_equalization_and_gamma_transform(img)
	# Filtros gaussianos, kernel = [3, 5, 7, 9]
	img_kern_3 = gaussian_low_pass_filter(img_eq_gam, 3)
	img_kern_5 = gaussian_low_pass_filter(img_eq_gam, 5)
	img_kern_7 = gaussian_low_pass_filter(img_eq_gam, 7)
	img_kern_9 = gaussian_low_pass_filter(img_eq_gam, 9)
	# Calcula imagem media a partir das imagens filtradas com gaussianas (kernel=[3, 5, 7, 9])
	img_media = average_img(img_kern_3, img_kern_5, img_kern_7, img_kern_9)
	# Binarization da imagem media por meio do NBIS-mindtct
	img_bi = binarization(img_media)
	######Outros Processos#######
	#
	#############################
	img_final = img_bi.copy()	#Mudar para: img_final = img_*.copy()
	# Salva imagem final como output/index_result.bmp
	fname='{}{}{}'.format('output/', index, '_result.bmp')
	cv2.imwrite(fname, img_final)
	# Concatena imagem inicial e final para comparar
	compare = np.concatenate((img, img_final), axis = 1)
	# Salva imagem concatenada como output/index_compare.bmp
	fname='{}{}{}'.format('output/', index, '_compare.bmp')
	cv2.imwrite(fname, compare)
	# Incrementa o indice da imagem
	index += 1