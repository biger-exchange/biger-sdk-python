#!/bin/sh
rootpath=$(pwd)
source ${rootpath}/pysdkenv/bin/activate
mkdir logs
python bgcli.py -c cfg/bgcli.py

