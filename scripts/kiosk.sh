#!/bin/bash
xset s 30 30
xset -dpms
unclutter -idle 0.5 -root &

sed -i 's/"exited_cleanly":false/"exited_cleanly":true/' /home/$USER/.config/chromium/Default/Preferences
sed -i 's/"exit_type":"Crashed"/"exit_type":"Normal"/' /home/$USER/.config/chromium/Default/Preferences


/usr/bin/chromium-browser --noerrdialogs --disable-infobars --kiosk http://localhost:3000 

