#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import sys
import threading
import webbrowser
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView
import multiprocessing
from flask import Flask, render_template, redirect, url_for, jsonify, request
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


if __name__ == '__main__':
    (web_push, web_pop) = multiprocessing.Pipe()
    web_service = threading.Thread(target=running_web)
    win_service = threading.Thread(target=running_win)
    web_service.setDaemon(True)
    web_service.start()
    win_service.start()
    win_service.join()







