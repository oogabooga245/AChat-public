AChat.pyw (Chat Client):
A GUI chat client using Tkinter.
Connects to a relay server at IP 69.164.196.248 on port 9000.
Sends and receives messages via a socket connection.
Displays chat messages in a text box.
Handles message sending on button click or pressing Enter.

Relay.py (Relay Server):

Accepts multiple client connections and relays messages.
Forwards received messages to all connected clients.
Can also connect to an upstream relay server.
Runs a server on 0.0.0.0:9000 and connects to the parent relay at 69.164.196.248:9000.
