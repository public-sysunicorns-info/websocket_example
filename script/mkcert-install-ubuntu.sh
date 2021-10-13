#!/usr/bin/env bash

sudo apt install libnss3-tools -y
sudo mkdir /opt/mkcert
sudo wget -P /opt/mkcert https://github.com/FiloSottile/mkcert/releases/download/v1.4.3/mkcert-v1.4.3-linux-amd64
sudo mv /opt/mkcert/mkcert-v1.4.3-linux-amd64 /opt/mkcert/mkcert
sudo chmod +x /opt/mkcert/mkcert

# install in ~/.local/share/mkcert
/opt/mkcert/mkcert -install

ln -s /opt/mkcert/mkcert /usr/local/bin/mkcert
