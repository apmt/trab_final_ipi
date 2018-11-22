from PIL import Image
import numpy as np
import math 

def teste(img, grau, fade):
        h = img.height
        w = img.width
        x = range(0, 500, 50)
        y = [100, 80, 60, 50, 50, 50, 50, 50, 50, 50, 50]
        p = np.polyfit(x,y,grau)
        polinomio = np.polyval(p,range(0, h, 1))
        somaFade = np.fliplr(range(0, 255, fade))
        tamSomaFade = np.size(somaFade)
        matriz = np.ones(h, w)*255
        cropped = np.array(matriz, np.uint8)

        for i in range(1, h, 1):
            for j in range(1, w, 1):
                if(j>polinomio[i] and j<(w-polinomio[i])):
                    cropped[i,j] = img[i,j]
                    if(math.ceil(j-polinomio[i])<=tamSomaFade[2]):
                        cropped[i,j] = cropped[i,j] + somaFade(math.ceil(j-polinomio[i]))
                    if(math.ceil((w-polinomio[i])-j) > 0 and math.ceil((w-polinomio[i])-j) <= tamSomaFade[2]):
                        cropped[i,j] = cropped[i,j] + somaFade(math.ceil((w-polinomio[i])-j))
                if(cropped[i,j] > 255):
                    cropped[i,j] = 255

        for j in range(1, w, 1):
            for i in range (1, tamSomaFade[2], 1):
                cropped[i,j] = cropped[i,j] + somaFade[i]
                if(cropped[i,j] > 255):
                    cropped[i,j] = 255

        for j in range(1, w, 1):
            for i in range((h-tamSomaFade[2]+1), h, 1):
                cropped[i,j] = cropped[i,j] + somaFade[i-h+tamSomaFade(2)]
                if(cropped[i,j] > 255):
                    cropped[i,j] = 255