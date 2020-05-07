#!/bin/bash

if [[ $EUID -ne 0 ]]; then
	echo "A scriptet csakis root jogosultsággal lehet futtatni, kérlek, futtasd sudo-val"
	exit 1
fi
mkdir -p ~/local
wget https://www.python.org/ftp/python/3.7.4/Python-3.7.4.tgz
tar -xf Python-3.7.4.tgz
cd Python-3.7.4
./configure
make
make altinstall prefix=~/local
ln -s ~/local/bin/python3.7 ~/local/bin/python
cd ..

apt-get update
apt-get install python3-pip
pip3 install numpy
pip3 install pytesseract
pip3 install opencv-python
