#!/bin/sh
#
# Usage
# ~~~~~
# sudo ./upgrade_to_v0.sh

# Setup dingo_ui service to display info on OLED on boot
cp dingo_ui_boot.service /etc/systemd/system
systemctl enable dingo_ui_boot.service

# Turn off OLED display as late as possible to signal its ok to pull power to the Pi
cp oled_power_off.sh /lib/systemd/system-shutdown/
chmod +x /lib/systemd/system-shutdown/oled_power_off.sh

systemctl daemon-reload
