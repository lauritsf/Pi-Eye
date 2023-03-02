import socket

from routes import *
from bottle import run

host = (
    socket.gethostname() + ".local"
)  # should be something like: pieye-spider.local, this is set when setting up the pieye

run(host=host, port=8080, debug=True, reloader=True)
