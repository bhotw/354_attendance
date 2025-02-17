
#!/bin/bash
cd "$HOME/attendance_user/354_attendance/back_end" || exit 1

source "$HOME/attendance_user/354_attendance/backend_env/bin/activate"

exec gunicorn -w 4 -b 0.0.0.0:5000 app:app
