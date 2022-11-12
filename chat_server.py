#!/usr/bin/python3
import select
import socket
import sys

# Server setup
s_server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
s_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s_server.bind(("", 7777))
s_server.listen(1)
socket_list = {s_server}
nick_dict = {}

# Get client's socket from its nickname
def GetKey(val):
    for key, value in nick_dict.items():
        if val == value:
            return key
    return "This is not supposed to happen!"

# Main loop
while True:
    sl, _, _ = select.select(socket_list, [], [])
    for s in sl:
        # Interaction with connected client
        if s != s_server:
            data = s.recv(1500)
            u_data = data.decode("utf-8").split(' ', maxsplit=1)
            s_addr = s.getpeername()
            # Check message syntax
            if len(u_data) == 1:
                cmd = u_data[0]
                msg = ""
            elif len(u_data) == 2:
                cmd, msg = u_data
            else:
                s.sendall("This is not supposed to happen!".encode("utf-8"))
            
            if cmd == "MSG":
                for i in range(1, len(socket_list)):
                    if socket_list[i] != s:
                        socket_list[i].sendall("[{}] {}".format(nick_dict[s].strip(),msg).encode("utf-8"))
                        
            elif cmd == "QUIT":
                # Bye bye message
                for i in range(1, len(socket_list)):
                    if socket_list[i] != s:
                        socket_list[i].sendall("[{}] {}".format(nick_dict[s].strip(), msg).encode("utf-8"))
                # Disconnection message
                for i in range(1, len(socket_list)):
                    socket_list[i].sendall("[{}] {}".format(nick_dict[s].strip()).encode("utf-8"))
                # Disconnecting the client
                del nick_dict[s]
                s.close()
                socket_list.remove(s)
            
            elif cmd == "NICK":
                # Key clients nickname to its socket
                nick_dict[s] = msg
                print("Client {}:{} => {}".format(s_addr[0], s_addr[1], msg))
            
            elif cmd == "NAMES":
                s.sendall("[SERVER]".encode("utf-8"))
                for value in nick_dict.values():
	                s.sendall(" {}".format(value).rstrip("\n").encode("utf-8"))
                s.sendall("\n".encode("utf-8"))
            
            elif cmd == "KILL":
                kill_split = msg.split(' ',maxsplit=1)
                if len(kill_split) == 1:
                    target = kill_split[0]
                    kill_msg = "You've been killed!"
                elif len(kill_split) == 2:
                    target, kill_msg = kill_split
                target_s = GetKey(target + "\n")
                target_s.sendall("[{}] {}".format(nick_dict[s].strip(), kill_msg).encode("utf-8"))
                del nick_dict[target_s]
                target_s.close()
                socket_list.remove(target_s)
                
            else:
                s.sendall("[SERVER] Wrong prefix used!\n".encode("utf-8"))
        else:
            sclient, addr = s_server.accept()
            socket_list.append(sclient)
            nick_dict[sclient] = "{}:{}".format(addr[0], addr[1])
            anonymous_i = anonymous_i + 1
            for i in range(1, len(socket_list)):
                if socket_list[i] != sclient:
                    socket_list[i].sendall("[SERVER] {}:{} has joined the chat\n".format(addr[0],addr[1]).encode("utf-8"))
            print("Client connected {}:{}".format(addr[0],addr[1]).strip())
