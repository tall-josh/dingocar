#!/bin/sh
#
# Usage
# ~~~~~
# sudo ./upgrade_to_v0.sh

cp dingo_ui_boot.service /etc/systemd/system
systemctl enable dingo_ui_boot.service

# Currently, 
cp dingo_ui_halt.service /etc/systemd/system
systemctl disable dingo_ui_halt.service

systemctl daemon-reload
