import glob
import cv2
from func import *
from clean import *

# Recebe todas imagens
images = glob.glob("Images/*.bmp")
index = 0
qnt_img = len(images)
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
	# Binarization das imagens por meio do NBIS-mindtct
	img_bi_1 = binarization(img_kern_3)
	img_bi_2 = binarization(img_kern_5)
	img_bi_3 = binarization(img_kern_7)
	img_bi_4 = binarization(img_kern_9)
	# Calcula imagem media a partir das imagens binarias filtradas com gaussianas (kernel=[3, 5, 7, 9])
	img_bi_media = average_bi(img_bi_1, img_bi_2, img_bi_3, img_bi_4)
	######Outros Processos#######
	#
	#############################
	img_final = img_bi_media.copy()	#Mudar para: img_final = img_*.copy()
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
	print "carregando", (index*100/qnt_img), "%"
print "imagens processadas em: /output"