from vanna.servers.fastapi import VannaFastAPIServer
from vanna_setup import agent

server = VannaFastAPIServer(agent)
app = server.create_app()
print("Routes:")
for route in app.routes:
    print(route.path, getattr(route, "methods", None))
