#!/usr/bin/env bash

source ~/.massa_profile


cd $MASSA_NODE_PATH
./massa-node -p $MASSA_PASS

cd - > /dev/null
exit 0
