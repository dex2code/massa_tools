#!/usr/bin/env bash

source ~/.massa_profile


function send_tg_message {
        curl -s --max-time 10 --retry 5 --retry-delay 2 --retry-max-time 10 \
        -X POST $TG_URL \
        -d chat_id=$TG_CHAT \
        -d text="$MASSA_NODE_NAME: $1" > /dev/null
}


# Check if node is online
NODE_CHAINID=$(python3 ~/bin/massa_checkalive.py)

if [[ $? == "0" ]]
then
        echo "Node seems online ($NODE_CHAINID)"
else
        echo "Node seems offline"
        send_tg_message "☠ Node seems offline!"
        exit 1
fi


# Check candidate rolls
CANDIDATE_ROLLS=$(python3 ~/bin/massa_checkrolls_candidate.py)

if [[ $? == "0" ]]
then
        if [[ $CANDIDATE_ROLLS -gt 0 ]]
        then
                echo "Candidate rolls positive ($CANDIDATE_ROLLS)"
        else
                echo "Candidate rolls negative ($CANDIDATE_ROLLS)"
                send_tg_message "⚠ Candidate rolls equals $CANDIDATE_ROLLS!"
        fi
else
        echo "Error candidate rolls"
        send_tg_message "🚨 Error getting number of candidate rolls!"
fi


# Check active rolls
ACTIVE_ROLLS=$(python3 ~/bin/massa_checkrolls_active.py)

if [[ $? == "0" ]]
then
        if [[ $ACTIVE_ROLLS -gt 0 ]]
        then
                echo "Active rolls positive ($ACTIVE_ROLLS)"
        else
                echo "Active rolls negative ($ACTIVE_ROLLS)"
                send_tg_message "⚠ Active rolls equals $ACTIVE_ROLLS!"
        fi
else
        echo "Error active rolls"
        send_tg_message "🚨 Error getting number of active rolls!"
fi


# Check final balance
FINAL_BALANCE=$(python3 ~/bin/massa_checkbalance.py)

if [[ $? == "0" ]]
then
        if [[ $FINAL_BALANCE -gt 0 ]]
        then
                echo "Balance positive ($FINAL_BALANCE)"
        else
                echo "Balance negative ($FINAL_BALANCE)"
                send_tg_message "⚠ Final balance equals $FINAL_BALANCE!"
        fi
else
        echo "Error balance"
        send_tg_message "🚨 Error getting final balance!"
fi


# Check ability to buy rolls
NUM_ROLLS=$(python3 ~/bin/massa_canbuyroll.py)

if [[ $? == "0" ]]
then
        if [[ $NUM_ROLLS -gt 0 ]]
        then
                echo "We can buy $NUM_ROLLS rolls more"
                ~/bin/massa_buyroll.sh $NUM_ROLLS $MASSA_FEE
                send_tg_message "💸 Tried to buy $NUM_ROLLS rolls more"
        else
                echo "We still cannot buy more rolls"
        fi


else
        echo "Error rolls number"
        send_tg_message "🚨 Error getting number of rolls to buy!"
fi


exit 0
