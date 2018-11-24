import os
import glob
import shutil
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

try:
	os.mkdir('./aux')
except OSError:
	shutil.rmtree('./aux')
	os.mkdir('./aux')

images = sorted(glob.glob("output/results/*.jpeg"))
i = 0
for image in images:
	os.system("nfiq {} >> aux/nfiq.log".format(image))
	os.system('mindtct {} aux/{}'.format(image, i))
	i += 1

xyt_files = sorted(glob.glob("aux/*.xyt"))
for i in xyt_files:
	for j in xyt_files:
		os.system('bozorth3 {} {} >> aux/boz3.log'.format(i, j))

arq_nfiq = open("aux/nfiq.log", "r")
infos = arq_nfiq.read().split()
infos = np.array(infos, dtype=int)
qualidade = Counter(infos)
for i in range (1, 6):
	if(qualidade[i]==0):
		qualidade[i]=0
keys = ["Excellent", "Very good", "Good", "Fair", "Poor"]
fig, axs = plt.subplots(1, 2, figsize=(13, 5))
axs[0].bar(keys, qualidade.values())
axs[0].set_title('Fingerprints quality')

arq_boz3 = open("aux/boz3.log", "r")
matriz = arq_boz3.read().split()
matriz = np.reshape(matriz, (len(xyt_files),len(xyt_files)))
matriz = matriz.astype(np.int)
matches = Counter(false_rejection=0, false_acceptance=0)
tresh = 18
for i in range (0, len(xyt_files)):
	for j in range (0, len(xyt_files)):
		if(matriz[i, j]>tresh):
			if(not(i%2!=0 and j==i-1) and not(i==j) and not(i%2==0 and j==i+1)):
				matches['false_acceptance']+=1
		else:
			if(i==j or (i%2!=0 and j==i-1) or (i%2==0 and j==i+1)):
				matches['false_rejection']+=1
axs[1].bar(matches.keys(), matches.values())
axs[1].set_title('Error Graph')
axs[1].set_ylim(0, 10)
plt.show()
try:
	shutil.rmtree('./aux')
except OSError:
	print 'erro: deleting auxiliar diretory ./aux'
