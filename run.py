
from attendance import app
import os


if __name__ == "__main__":
    host = os.environ.get('354_ATTENDANCE', '0.0.0.0')
    port = int(os.environ.get('354_ATTENDANCE_PORT', 5000))

    app.run(host=host, port=port, debug=True)
