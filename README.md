# Chat Server
Basic chat server made for a university networking class using the UNIX `select()` syscall to manage multiple clients.\
\
How to launch the server : \
`python3 chat_server.py <port>` \
\
**List of available client commands :**
- `NICK <nickname>` : set nickname.
- `NAMES` : ask the server for the nickname list of of all connected clients.
- `MSG <message>` : send a message to all connected clients.
- `KILL <nickname> <message>` : disconnect a client after sending him a message.
- `QUIT <message>` : send a last message before quitting and being disconnected form the server.

**List of standard behaviour :**
- `<ip>:<port>` : default nickname
