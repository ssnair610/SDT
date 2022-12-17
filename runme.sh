# !/bin/bash
# !/bin/bash
pip install argparse
pip install tqdm
pip install npm

read -p "initiate server setup?(Y/N):" setup_mode

if [ $setup_mode -eq "Y" ] then
    if [ $# -eq 1 ] then
        ./server-side/calibrate.py $1
    elif [ $# -gt 1 ] then
        ./server-side/calibrate.py $1 -p $2
    else
        echo "Setup incomplete. Run `python -u server-side/calibrate.py with network adapter name to calibrate server connection."
fi
