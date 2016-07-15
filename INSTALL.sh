# !/bin/bash

python -B setup.py build
sudo cp -r ./xBackLight /usr/share/
sudo cp run_BackLight.sh /etc/init.d/
