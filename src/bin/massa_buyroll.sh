#!/usr/bin/env bash

source ~/.massa_profile


if [[ $# -ne 2 ]]
then
        echo "Error! No Rolls number or Network fee value given!"
        echo "Usage: $0 <Rolls_number> <Network_fee>"
        exit 1
fi

cd $MASSA_CLIENT_PATH
./massa-client -p $MASSA_PASS buy_rolls $MASSA_WALLET $1 $2

cd - > /dev/null
exit 0
