#! bin/bash

sudo apt update && sudo apt upgrade -y
sudo apt install qrencode wireguard python3-venv git
git clone https://github.com/Nikolailavr/WireguardServ.git
cd WireguardServ

rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -U pip
pip install -r requirements.txt
deactivate