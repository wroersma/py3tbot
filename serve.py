from tbot.py3tbot import Py3TBOT
import os
Py3TBOT = Py3TBOT()

app = Py3TBOT.create_app()
app.secret_key = os.urandom(12)
app.run(debug=True, threaded=True, host="127.0.0.1", port=8080)
