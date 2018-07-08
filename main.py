#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import sys
import queue
import socket
import threading
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from flask import Flask, render_template, redirect, jsonify, request
from socket_module import SocketService

web = Flask(__name__)
socket_service = None


@web.route('/index')
@web.route('/')
def index():
    return render_template('index.html')


@web.route('/login')
def login():
    global socket_service
    socket_service = SocketService()
    socket_service.init()
    return redirect('/app')


@web.route('/app')
def appx():
    return render_template('app.html')


@web.route('/send', methods=['POST'])
def send():
    message_data = {
        'nickname': request.form.get('nickname'),
        'message': request.form.get('message')
    }
    print(message_data)
    global socket_service
    socket_service.send(json.dumps(message_data))
    return jsonify({'status': 'success'})


@web.route('/recv')
def recv():
    global socket_service
    message_list = socket_service.recv()
    message_list['status'] = 'success'
    print(message_list)
    return json.dumps(message_list)


def running_web():
    global web
    web.run()


def running_win():
    app = QApplication(sys.argv)
    browser = QWebEngineView()
    browser.load(QUrl("http://127.0.0.1:5000"))
    browser.show()
    app.exec_()


class SocketService:
    PORT = 12877
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
        message_num = 0
        while self.recv_data.qsize() > 0:
            message_list[len(message_list)]=json.loads(self.recv_data.get())
            message_num += 1
        message_list['message_num']=message_num
        return message_list


if __name__ == '__main__':
    win_service = threading.Thread(target=running_win)

    web_service = threading.Thread(target=running_web)

    web_service.setDaemon(True)
    web_service.start()
    win_service.start()
    win_service.join()







