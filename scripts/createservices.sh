#!/bin/bash

echo "Creating systemd services..."

# Kiosk Service
cat <<EOL | sudo tee /etc/systemd/system/kiosk.service
[Unit]
Description=Kiosk Mode for Chromium
After=network.target

[Service]
ExecStart=/home/attendance_user/354_attendance/scripts/kiosk.sh
Restart=always
User=$USER
Group=$USER
Environment=DISPLAY=:0
Environment=XAUTHORITY=/home/$USER/.Xauthority

[Install]
WantedBy=multi-user.target
EOL

echo "kiosk.service created!"

# Frontend Service
cat <<EOL | sudo tee /etc/systemd/system/frontend.service
[Unit]
Description=Frontend Service
After=network.target

[Service]
ExecStart=/home/attendance_user/354_attendance/scripts/frontend.sh
Restart=always
User=$USER
Group=$USER

[Install]
WantedBy=multi-user.target
EOL

echo "frontend.service created!"

# Backend Service
cat <<EOL | sudo tee /etc/systemd/system/backend.service
[Unit]
Description=Backend Service
After=network.target postgresql.service

[Service]
ExecStart=/home/attendance_user/354_attendance/scripts/backend.sh
Restart=always
User=$USER
Group=$USER

[Install]
WantedBy=multi-user.target
EOL

echo "backend.service created!"

# Reload systemd to recognize the new services
sudo systemctl daemon-reload

echo "All services have been created. You can now enable and start them."


echo "Enabling and starting services..."
sudo systemctl daemon-reload
sudo systemctl enable kiosk.service frontend.service backend.service
sudo systemctl start kiosk.service frontend.service backend.service

echo "All services are running!"
