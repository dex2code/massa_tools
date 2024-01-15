#!/usr/bin/env bash

source ~/.massa_profile


journalctl -f -u massad.service

exit 0
