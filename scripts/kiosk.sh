#!/bin/bash
xset s 30 30
xset -dpms
unclutter -idle 0.5 -root &

sed -i 's/"exited_cleanly":false/"exited_cleanly":true/' /home/$USER/.config/chromium/Default/Preferences
sed -i 's/"exit_type":"Crashed"/"exit_type":"Normal"/' /home/$USER/.config/chromium/Default/Preferences


/usr/bin/chromium-browser --noerrdialogs --disable-infobars --kiosk http://localhost:3000 


show_clock() {

  xterm -fullscreen -fa 'Monospace' -fs 48 -bg black -fg white -e "

  while true; do
    clear
    date +"%H:%M:%S" | figlet -c
    sleep 1

    if [ $(xprintidel) -lt 60000 ]; then
      break
    fi

  done
  " &
  CLOCK_PID=$!
  wait $CLOCK_PID
}

While true; do
  sleep 5
  if [ $(xprintidel) -gt 60000 ]; then
    show_clock
  fi
done