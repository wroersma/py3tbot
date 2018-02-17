import os
from app import create_app, db, cli
from app.models import User, Message, Notification, Task

app = create_app()
app.secret_key = os.urandom(12)
app.run(debug=True, threaded=True, host="127.0.0.1", port=8080)
