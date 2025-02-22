# 354_attendance
app for attendance tacking for our team. 


- Your pi needs to have the SPI and I2C interface enable and SSH(optional).
- Make sure the username is: attendance_user
- the repo need to be in /home/attendance_user/
- then run chmod +x setup.sh
- then run ./setup.sh
- it will ask for postgres username, password, and database name
- then it will create a new postgesql user database 
- And then it will also create a .env file with teh postgresql DB_URL
- Then it will ask for admin username, email, and password for the attendance system.
- Once this is done you can reboot your system, and it should boot into kiosk mode
- You can access the admin my going to localhost:3000/admin.
