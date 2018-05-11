#!/usr/bin/python3
# -*- coding: utf-8 -*-
import time
import json
import socket
import threading
import queue


class SocketService:
    PORT = 12888
    MODE = '<broadcast>'

    send_client = None
    recv_client = None
    recv_data = queue.Queue(maxsize=1024)
    recv_threading = None

    def init(self):
        if self.send_client is not None:
            self.send_client.shutdown(2)
            self.send_client.close()
            self.send_client = None
        self.send_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.send_client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        if self.recv_client is not None:
            self.recv_client.shutdown(2)
            self.recv_client.close()
            self.recv_client = None
        self.recv_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.recv_client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.recv_client.bind(('', self.PORT))
        self.recv_threading = threading.Thread(target=SocketService.recving, args=(self.recv_client, self.recv_data,))
        self.recv_threading.start()

    def send(self, message):
        message = message.encode('utf-8')
        self.send_client.sendto(message, (self.MODE, self.PORT))

    def recving(client, data):
        while True:
            net_data, net_address = client.recvfrom(65535)
            net_data = net_data.decode('utf-8')
            data.put(net_data)

    def recv(self):
        message_list = {}
        while self.recv_data.qsize() > 0:
            message_list['mid'+len(message_list)]=json.loads(self.recv_data.get())
        return message_list


if __name__ == '__main__':
    s = SocketService()
    s.init()
    while True:
        str = input("Input:")
        s.send(str)
        time.sleep(1)
        print(s.recv_data)
