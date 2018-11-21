# trab_final_ipi

# VERSIONS
numpy 1.15.3\\
cv2 2.4.9.1\\
Python 2.7.12\\

# NBIS

Baixar NBIS_5.0.0: http://nigos.nist.gov:8080/nist/nbis/nbis_v5_0_0.zip

Unzip nbis_v5_0_0.zip

No terminal:

$ sudo apt-get install cmake libc6-dev libc6-dev-i386 g++-multilib

$ sudo apt-get install libx11-dev

$ sudo mkdir /usr/local/NBIS/Main

$ cd Rel_5.0.0

$ ./setup.sh /usr/local/NBIS/Main --64 #(or --32)

$ sudo make config

$ sudo make it

$ sudo install LIBNBIS=yes
	Op:Add path toda vez que executar o programa:
		$ export PATH=$PATH:/usr/local/NBIS/Main/bin
	OBS:Add path permanente:
		$ gedit.bashrc
		No final do arquivo copie:
		export PATH=$PATH:/usr/local/NBIS/Main/bin
		Clique em salvar e depois:
		$ source .bashrc
		Feche o terminal, abra denovo e verifique com:
		$ echo $PATH

# executar:
$ python main.py

# excluir output imagens:
$ python clean.py
 
