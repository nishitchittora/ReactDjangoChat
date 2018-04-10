from channels import include
from chat import consumers

# channel_routing = [
#     include("chat.routing.websocket_routing", path=r"^/chat/stream"),
#     include("chat.routing.custom_routing"),
# ]

channel_routing = {
    'websocket.connect': consumers.ws_connect,
    'websocket.receive': consumers.ws_receive,
    'websocket.disconnect': consumers.ws_disconnect,
}