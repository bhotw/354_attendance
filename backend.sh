
#!/bin/bash
cd "$HOME/354_attendance/back_end" || exit 1

source "$HOME/flask_react_env/bin/activate"

exec python app.py
