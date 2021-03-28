#!/bin/bash
BASEDIR=/opt/nordvpn-client
CMD="$BASEDIR/venv/bin/python3 $BASEDIR/nordvpn.py $1"

cd $BASEDIR
SERVER=`$CMD`

FILE="$BASEDIR/configs/$SERVER"
echo $FILE

openvpn $FILE
