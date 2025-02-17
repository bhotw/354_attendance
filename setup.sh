#!/bin/bash

# Ensure scripts are executable
chmod +x ./scripts/installev.sh
chmod +x ./scripts/createenv.sh
chmod +x ./scripts/kiosk.sh
chmod +x ./scripts/frontend.sh
chmod +x ./scripts/backend.sh
chmod +x ./scripts/createservices.sh

# Run the scripts sequentially
echo "Running installation scripts..."
./scripts/installev.sh
./scripts/createenv.sh
./scripts/kiosk.sh
./scripts/frontend.sh
./scripts/backend.sh
./scripts/createservices.sh

echo "Setup completed!"
