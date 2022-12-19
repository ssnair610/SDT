# !/bin/bash
pip install argparse
pip install tqdm
pip install npm

read -p "Initiate server setup? (Y/N)" yn
case $yn in
    [Yy]* )
        if [ $setup_mode -eq "Y" ] then
            read -p "provide network adapter:" adapter
            $error = `./server-side/calibrate.py $adapter`

            if [$error -eq 0 ] then
                echo "server Setup incomplete. Run `python -u server-side/calibrate.py` with network adapter name to calibrate server connection."
            fi
        fi
    * ) 
        echo "Server setup ignored. Run `python -u server-side/calibrate.py` with network adapter name to calibrate server connection if needed.";;
esac