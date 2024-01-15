#!/usr/bin/env bash

source ~/.massa_profile


cd $MASSA_CLIENT_PATH
./massa-client -p $MASSA_PASS get_addresses $MASSA_WALLET

cd - > /dev/null
exit 0
