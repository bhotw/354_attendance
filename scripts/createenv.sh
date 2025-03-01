#!/bin/bash


read -p "Enter the database username: " DB_USER
read -sp "Enter the database password: " DB_PASS
read -p "Enter the database name: " DB_NAME

PG_VERSION=$(ls /etc/postgresql/ | sort -V | tail -n 1)
PG_HBA="/etc/postgresql/$PG_VERSION/main/pg_hba.conf"


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


echo "Updating pg_hba.conf to allow local network access..."
if ! grep -q "192.168.1.0/24   md5" "$PG_HBA"; then
    echo "host    all   all   192.168.1.0/24   md5" | sudo tee -a "$PG_HBA"
    echo "Restarting PostgreSQL to apply changes..."
    sudo systemctl restart postgresql
else
    echo "pg_hba.conf already contains the required entry. No changes made."
fi

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
