from flask import Flask, request, send_from_directory
from waitress import serve
import os
import time

home = os.environ['HOME']

import former.save
from former.formparser import parse

app = Flask(__name__, static_url_path='/static', static_folder='static')

cache = {}

@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

@app.route('/<form>', methods=['GET', 'POST'])
def index(form):
    if request.method == 'POST':
        if form not in cache:
            return 'form doesn\'t exist'
        save.parse(form, cache[form][0], dict(request.form))
        return cache[form][1]
    else:
        if form not in cache:
            path = f'{home}/.former/{form}.yml'
            print(path)
            if os.path.exists(path) and os.path.exists(path):
                cache[form] = parse(path)
            else:
                return 'Form not found'
        return cache[form][1]


def run():
    serve(app, host='127.0.0.1', port=5000)
