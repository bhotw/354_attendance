#!/bin/bash

echo "Updating package lists..."
sudo apt update -y

echo "Installing Python, venv, and pip..."
sudo apt install -y python3 python3-venv python3-pip

echo "Installing PostgreSQL..."
sudo apt install -y postgresql postgresql-contrib

echo "Installing Node.js and npm..."
sudo apt install -y nodejs npm

echo "Ensuring latest stable Node.js version..."
sudo npm install -g n
sudo n stable

echo "Installing dependencies from admin/package.json..."
cd admin
npm install

echo "Installation completed!"