#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
from flask import Flask, render_template, redirect, url_for, jsonify, request
from socket_module import SocketService
app = Flask(__name__)
socket_service = None


@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    global socket_service
    socket_service = SocketService()
    socket_service.init()
    return redirect('/app')


@app.route('/app')
def appx():
    return render_template('app.html')


@app.route('/send',methods=['POST'])
def send():
    message_data = {
        'nickname': request.form.get('nickname'),
        'message': request.form.get('message')
    }
    print(message_data)
    global socket_service
    socket_service.send(json.dumps(message_data))
    return jsonify({'status': 'success'})


@app.route('/recv')
def recv():
    global socket_service
    message_list = socket_service.recv()
    message_list['status']='success'
    print(message_list)
    return jsonify(message_list)


if __name__ == '__main__':
    app.run()

