#!/bin/bash

echo "Updating package lists..."
sudo apt update -y

echo "Installing Python, venv, and pip..."
sudo apt install -y python3 python3-venv python3-pip

echo "Installing PostgreSQL..."
sudo apt install -y postgresql postgresql-contrib

echo "Installation completed!"
