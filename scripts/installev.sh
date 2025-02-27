#!/bin/bash

echo "Updating package lists..."
sudo apt update -y

echo "Installing Python, venv, and pip..."
sudo apt install -y python3 python3-venv python3-pip

echo "Installing PostgreSQL..."
sudo apt install -y postgresql postgresql-contrib

echo "Installing xprintidle... and figlet...."
sudo apt-get install xprintidle

echo "Installing figlet...."
sudo apt-get install figlet

echo "Installing xterm..."
sudo apt-get install xterm


echo "Installing Node.js and npm..."
sudo apt install -y nodejs npm

echo "Ensuring latest stable Node.js version..."
sudo npm install -g n
sudo n stable

sudo npm install -g serve

echo "Installing dependencies from admin/package.json..."
cd admin
npm install
npm run build

echo "Installation completed!"