#!/usr/bin/env python
# -- coding:utf-8 --


import socket

udp_server_address = "127.0.0.1"
udp_port = 6789
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((udp_server_address, udp_port))
while True:
    data, addr = server_socket.recvfrom(1024)
    print("Message: ", data)
