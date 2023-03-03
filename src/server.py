import socket
import numpy as np
from routes import *
from bottle import run

host = (
    socket.gethostname() + ".local"
)  # should be something like: pieye-ant.local, this is set when setting up the pieye

hostnames = [
    "pieye-ant",
    "pieye-beetle",
    "pieye-cicada",
    "pieye-dragonfly",
    "pieye-earwig",
]
assert socket.gethostname() in hostnames

port = 8080 + np.where(np.array(hostnames) == socket.gethostname())[0][0]

run(host=host, port=port, debug=True, reloader=True)
