#!/usr/bin/env bash

source ~/.massa_profile


cd $MASSA_CLIENT_PATH
./massa-client -p $MASSA_PASS

cd - > /dev/null
exit 0
