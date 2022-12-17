# !/bin/bash
pip install argparse
pip install tqdm
pip install npm

read -p "initiate server setup?(Y/N):" setup_mode

if [ $setup_mode -eq "Y" ] then
    read -p "provide network adapter:" adapter
        ./server-side/calibrate.py adapter
else
    echo "Setup incomplete. Run `python -u server-side/calibrate.py with network adapter name to calibrate server connection."
fi
