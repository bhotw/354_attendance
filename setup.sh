#!/bin/bash

echo "Making all scripts executable..."
chmod +x installev.sh createenv.sh kiosk.sh frontend.sh backend.sh createservices.sh

echo "Running installation scripts..."
./installev.sh
./createenv.sh
./kiosk.sh
./frontend.sh
./backend.sh
./createservices.sh

echo "Setup completed!"
