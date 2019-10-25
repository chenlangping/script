#!/usr/bin/env python
# -- coding:utf-8 --


import socket
udp_server_address = "127.0.0.1"
udp_port = 6789
message = b"Hello server!"
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.sendto(message, (udp_server_address, udp_port))