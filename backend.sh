
#!/bin/bash
cd "$HOME/354_attendance/back_end" || exit 1

source "$HOME/flask_react_env/bin/activate"

exec gunicorn -w 4 -b 0.0.0.0:5000 app:app
