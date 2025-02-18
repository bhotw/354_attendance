#!/bin/bash

# Prompt user for DB credentials
read -p "Enter the database username: " DB_USER
read -sp "Enter the database password: " DB_PASS
read -sp "Enter the database password: " DB_NAME
PG_HBA="/etc/postgresql/$(psql -V | awk '{print $3}' | cut -d'.' -f1,2)/main/pg_hba.conf"
# Inform the user about the chosen credentials
echo "Using the following credentials:"
echo "DB_USER=$DB_USER"
echo "DB_PASS=$DB_PASS"
echo "DB_NAME=$DB_NAME"
echo "Creating PostgreSQL user and database..."
sudo -u postgres psql <<EOF
CREATE USER $DB_USER WITH PASSWORD '$DB_PASS';
CREATE DATABASE $DB_NAME OWNER $DB_USER;
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
EOF

# Run table_creation.py to create tables or any necessary setup
echo "Updating pg_hba.conf to allow local network access..."
echo "host    all   all   192.168.1.0/24   md5" | sudo tee -a $PG_HBA

echo "Creating virtual environment..."
python3 -m venv backend_env

echo "Activating virtual environment..."
source backend_env/bin/activate

echo "Installing requirements..."
pip install -r requirements.txt

cd /home/attendance_user/354_attendance/back_end
echo "Creating ./back_end/.env file..."
cat <<EOL | sudo tee > .env
DB_URL=postgresql://$DB_USER:$DB_PASS@localhost:5432/$DB_NAME
EOL

echo "Running table_creation.py script..."
python3 /home/attendance_user/354_attendance/back_end/table_creation.py

echo "Add Admin user for the System."
python3 /home/attendance_user/354_attendance/back_end/add_admin_user.py

echo "Attendance setup complete!!!"
