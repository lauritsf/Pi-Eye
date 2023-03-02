from bottle import run
from fake_routes import *

run(host="127.0.0.1", port=8080, debug=True, reloader=True)
