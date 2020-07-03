from flask import Flask, request
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent
from waitress import serve

import former.formrender as formrender
import former.save
import time

app = Flask(__name__, static_url_path='', static_folder='static')

document = ''

class SourceEventHandler(FileSystemEventHandler):
    def __init__(self, post_url, src_file):
        self.post = post_url
        self.src = src_file

    def on_modified(self, event: FileModifiedEvent):
        global document
        document = formrender.build(self.post, self.src)

@app.route('/')
def index():
    return document

@app.route('/post', methods=['POST'])
def post():
    save.parse(dict(request.form))
    return 'ok'

def run(post_url = '/post', src_file = 'test.md'):
    global document
    document = formrender.build(post_url, src_file) 

    handler = SourceEventHandler(post_url, src_file)
    observer = Observer()
    observer.schedule(handler, src_file)
    observer.start()

    serve(app, host='127.0.0.1', port=5000)
    observer.stop()
    observer.join()
