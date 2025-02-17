#!/bin/bash

DB_USER="backend_user"
DB_PASS="backend_pass"
DB_NAME="backend_db"

echo "Creating PostgreSQL user and database..."
sudo -u postgres psql <<EOF
CREATE USER $DB_USER WITH PASSWORD '$DB_PASS';
CREATE DATABASE $DB_NAME OWNER $DB_USER;
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
EOF

echo pwd
echo "Creating virtual environment..."
python3 -m venv backend_env

echo "Activating virtual environment..."
source backend_env/bin/activate
echo pwd
echo "Installing requirements..."
pip install -r requirements.txt

cd back_end
echo "Creating ./back_end/.env file..."
cat <<EOL > ./back_end/.env
DB_URL=postgresql://$DB_USER:$DB_PASS@localhost:5432/$DB_NAME
EOL

echo "Virtual environment setup complete!"
